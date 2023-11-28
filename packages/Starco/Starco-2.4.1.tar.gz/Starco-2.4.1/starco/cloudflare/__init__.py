import CloudFlare
class CloudFlareHandler:
    def __init__(self,email,api) -> None:
        self.cf = CloudFlare.CloudFlare(email,token=api)
    def get_dns_records(self,domain):
        params = {'name': domain}
        zones = self.cf.zones.get(params=params)
        zone = [i for i in zones if i['name']==domain]
        if not zone:
            raise Exception('domain not exists')
        zone_id = zone[0]['id']
        dns_records = self.cf.zones.dns_records.get(zone_id)
        return dns_records
        
    def update_dns_records(self,domain,sub,record_type,new_content=None,new_type=None,proxy:bool=None):
        record_type = record_type.upper()
        if new_type:new_type.upper()
        params = {'name': domain}
        zones = self.cf.zones.get(params=params)
        zone = [i for i in zones if i['name']==domain]
        if not zone:
            raise Exception('domain not exists')
        zone_id = zone[0]['id']
        if '.' not in sub:sub=sub+f".{domain}"
        
        dns_records = self.cf.zones.dns_records.get(zone_id)
        dns_records = [i for i in dns_records if i['name']==sub and i['type']==record_type]
        if not dns_records:
            raise Exception('dns_records not exists')
        record = dns_records[0]
        if not new_content:new_content=record['content']
        if not new_type:new_type=record['type']
        
        data={'name':record['name'],'content':new_content,'type':new_type,}
        if proxy!=None:
            data['proxied']=proxy
        
        self.cf.zones.dns_records.put(zone_id,record['id'],data=data)
        if self.purge_cache(zone_id):
            return True
        raise Exception('cache dont be purged')
    
    def purge_cache(self,zone_id=None,domain=None):
        if not zone_id and not domain:
            raise Exception('fill one of inputs parameters')
        if not zone_id:
            params = {'name': domain}
            zones = self.cf.zones.get(params=params)
            zone = [i for i in zones if i['name']==domain]
            if not zone:
                raise Exception('domain not exists')
            zone_id = zone[0]['id']
        
        self.cf.zones.purge_cache.post(zone_id,data={'purge_everything':True})
        return True
        
    def delete_dns_records(self,domain,sub,record_type):
        record_type = record_type.upper()
        params = {'name': domain}
        zones = self.cf.zones.get(params=params)
        zone = [i for i in zones if i['name']==domain]
        if not zone:
            raise Exception('domain not exists')
        zone_id = zone[0]['id']
        if '.' not in sub:sub=sub+f".{domain}"
        
        dns_records = self.cf.zones.dns_records.get(zone_id)
        dns_records = [i for i in dns_records if i['name']==sub and i['type']==record_type]
        if not dns_records:
            raise Exception('dns_records not exists')
        record = dns_records[0]
        
        self.cf.zones.dns_records.delete(zone_id,record['id'])
        if self.purge_cache(zone_id):
            return True
        raise Exception('cache dont be purged')
        
    def add_dns_records(self,domain,sub,record_type,content,proxy:bool=None):
        record_type = record_type.upper()
        params = {'name': domain}
        zones = self.cf.zones.get(params=params)
        zone = [i for i in zones if i['name']==domain]
        if not zone:
            raise Exception('domain not exists')
        zone_id = zone[0]['id']
        if '.' not in sub:sub=sub+f".{domain}"
        
        
        
        data={'name':sub,'content':content,'type':record_type}
        if proxy!=None:
            data['proxied']=proxy
        
        self.cf.zones.dns_records.post(zone_id,data=data)
        return True
    
    def get_all_domain(self):
        cf = self.cf
        zones = cf.zones.get()
        return [i['name'] for i in zones]
if __name__ == "__main__":
    api = '190ffb1842cf0fa55886cc0622803ed17ef0c'
    # token= 'JEWrIf5xnQP3SXlFqIIt8MiCwY80Q3dN-2EALo1p'
    # cert='v1.0-b954a062aef284635f66aab1-94d0ebae5d55c9f0a326ebdd89b1b5ec9e124df22bce16a9cc10d2180c144a2f6bb09489f1dc81075382d696f4e208065574a7c12892cb6de54d32cec0d24c317626ff349c2bd14a89'
    domain='smartrad.shop'
    cf = CloudFlareHandler('m.tahmasbi0111@yahoo.com',api=api)
    # o= [(i['name'],i['type']) for i in cf.get_dns_records(domain)]
    # cf.add_dns_records(domain,'foo','cname','ip1.smartrad.shop')
    o=cf.get_all_domain()
    print(o)
    # cf.update_dns(domain,'foo','cname','ip1.smartrad.shop',proxy=True)
    # cf.purge_cache(domain)
    