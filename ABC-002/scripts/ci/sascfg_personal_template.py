# sascfg_personal.py template for SASPy with SAS 9.4 training environment.
# Do not commit real credentials. Use .authinfo or secured GitLab CI/CD variables.
SAS_config_names = ['iom', 'local']
iom = {
    'java': '/usr/bin/java',
    'iomhost': 'sasclient.race.sas.com',
    'iomport': 8591,
    'encoding': 'utf-8',
    'authkey': 'sas94_iom'
}
local = {
    'saspath': '/opt/sas94/SASFoundation/9.4/sas',
    'encoding': 'utf-8'
}
