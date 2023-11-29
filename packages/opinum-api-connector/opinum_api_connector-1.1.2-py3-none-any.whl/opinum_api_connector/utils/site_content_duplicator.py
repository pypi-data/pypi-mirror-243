import logging
from copy import deepcopy

from opinum_api_connector import ApiConnector

logging.basicConfig(level=logging.INFO)


def default_source_callback(source, target_site):
    return source


class SiteContentDuplicator:
    """
    SiteContentDuplicator allows make a full copy of a site

    This implies a copy of all sources in the site with their variables (raw and calculated)
    """
    def __init__(self, target_site_ids, template_site_id, source_key_field, account_id=None,
                 source_callback=default_source_callback, update=False):
        """

        :param target_site_ids: a list of site ids that will host the new sources
        :param template_site_id: the site id that we copy
        :param source_key_field: allows to identify the sources: 'name', 'serialNumber', 'meternumber' or 'eanNumber'
        :param account_id: the tenant id
        :param source_callback: a method that transforms the source received input. Manipulating the source_key_field is allowed.
        :param update: to force updates
        """
        logging.info('Start Site Duplicator')
        self.target_site_ids = target_site_ids
        self.template_site_id = template_site_id
        self.source_key_field = source_key_field
        self.source_callback = source_callback
        self.update = update
        self.api_connector = ApiConnector(account_id=account_id)
        self.template_sources = list()
        self.template_vars = dict()
        self.template_var_id_infos = dict()
        for source in self.api_connector.get('sources',
                                             siteId=self.template_site_id,
                                             displayLevel='Site').json():
            logging.info(f"Getting info for source {source[self.source_key_field]}")
            self.template_sources.append(source)
            self.template_vars[source[self.source_key_field]] = dict()
            for variable in self.api_connector.get('variables',
                                                   sourceId=source['id'],
                                                   displayLevel='Verbose').json():
                logging.info(f"\tGetting info for variable {variable['mappingConfig']}")
                self.template_vars[source[self.source_key_field]][variable['mappingConfig']] = variable
                self.template_var_id_infos[variable['id']] = {
                    'source': source,
                    'variable': variable
                }

    def run(self):
        for site_id in self.target_site_ids:
            site = self.api_connector.get('sites', siteIds=[site_id], displayLevel='VerboseSite').json()[0]
            existing_sources = {s[self.source_key_field]: s for s in self.api_connector.get('sources',
                                                                                            siteId=site_id,
                                                                                            displayLevel='Site').json()}
            source_key_mappings = dict()
            for source in self.template_sources:
                # key for new source can be different with template
                new_source = self.source_callback(deepcopy(source), site)
                source_key = new_source[self.source_key_field]
                logging.info(f"Checking source {source_key}")
                new_source.pop('siteName')
                new_source['siteId'] = site_id
                if source_key not in existing_sources:
                    logging.info("\tCreating source")
                    new_source.pop('id')
                    existing_sources[source_key] = self.api_connector.post('sources', data=new_source).json()
                elif self.update:
                    logging.info("\tUpdating source")
                    new_source['id'] = existing_sources[source_key]['id']
                    self.api_connector.put(f"sources/{new_source['id']}", data=new_source)

                source_key_mappings[source[self.source_key_field]] = source_key

            # Second run now that all sources exist
            calculated_variables_templates = dict()
            existing_variables = dict()
            for source_key, source in existing_sources.items():
                logging.info(f"Checking variables for source {source_key}")
                existing_variables[source_key] = {v['mappingConfig']: v for v in self.api_connector.get('variables',
                                                                                                        sourceId=source['id'],
                                                                                                        displayLevel='Verbose').json()}
                for mapping, variable in self.template_vars[source[self.source_key_field]].items():
                    new_var = deepcopy(variable)
                    new_var['sourceId'] = source['id']
                    if mapping in existing_variables[source_key]:
                        if self.update:
                            new_var_id = existing_variables[source_key][mapping]['id']
                            new_var['id'] = new_var_id
                            if 'calculated' in new_var:
                                calculated_variables_templates.setdefault(source_key, list()).append(variable)
                                new_var['calculated']['calculatedVariableFormulas'] = [{}]
                            logging.info(f"\tUpdating variable {mapping}")
                            self.api_connector.put(f"sources/{source['id']}/variables/{new_var_id}", data=new_var)
                    else:
                        if 'calculated' in new_var:
                            # Keep another copy for later
                            calculated_variables_templates.setdefault(source_key, list()).append(variable)
                            new_var['calculated']['calculatedVariableFormulas'] = [{}]
                        new_var.pop('id')
                        logging.info(f"\tCreating variable {mapping}")
                        existing_variables[source_key][mapping] = self.api_connector.post(f"variables/source/{source['id']}",
                                                                                          data=new_var).json()

            # Third run now that all variables exist (without calculations possibly)
            for source_key, variables in calculated_variables_templates.items():
                source = existing_sources[source_key]
                logging.info(f"Finalising calculated variables for source {source_key}")
                for new_var in variables:
                    mapping = new_var['mappingConfig']
                    logging.info(f"\tUpdating variable {mapping}")
                    new_var_id = existing_variables[source_key][mapping]['id']
                    new_var['id'] = new_var_id
                    new_var['sourceId'] = source['id']
                    for formula in new_var['calculated']['calculatedVariableFormulas']:
                        for sub_var in formula['variables']:
                            if sub_var['siteId'] != self.template_site_id:
                                continue
                            sub_source_info = self.template_var_id_infos[sub_var['variableId']]
                            sub_var['siteId'] = site_id
                            sub_source_key = source_key_mappings[sub_source_info['source'][self.source_key_field]]
                            sub_var['sourceId'] = existing_sources[sub_source_key]['id']
                            sub_mapping = sub_source_info['variable']['mappingConfig']
                            sub_var['variableId'] = existing_variables[sub_source_key][sub_mapping]['id']
                        for form_value in formula['entities']:
                            form_value['siteId'] = site_id
                            sub_source_info = self.template_var_id_infos[sub_var['variableId']]
                            sub_source_key = source_key_mappings[sub_source_info['source'][self.source_key_field]]
                            form_value['sourceId'] = existing_sources[sub_source_key]['id']
                            form_value['entityId'] = existing_sources[sub_source_key]['id']
                    self.api_connector.put(f"sources/{source['id']}/variables/{new_var_id}", data=new_var)
                    existing_variables[mapping] = new_var



