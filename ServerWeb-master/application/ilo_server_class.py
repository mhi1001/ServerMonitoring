import hpilo

class Server_Ilo:

    def __init__(self, ip, ilouser, ilopass):
        self.ip = ip
        self.ilouser = ilouser
        self.ilopass = ilopass
        self.ilo = hpilo.Ilo(ip, ilouser, ilopass)

    def get_serial_no(self):

        host_data = self.ilo.get_host_data()
        # Response is a list, where the last element contains a dictionary with Serial Number as key
        # https://seveas.github.io/python-hpilo/info.html?highlight=serial
        return host_data.pop()["Serial Number"]
    
    def get_prod_name(self):
        return self.ilo.get_product_name()
    
    def get_power_reading(self):
        """ Returns power readings in the following order: average, present, min, max"""
        # Returns a dictionary where the value is a tuple of ints and strings E.g (65, "Watts")
        power_readings = self.ilo.get_power_readings()
        
        power_result = {"powerAverage": power_readings['average_power_reading'][0],
                        "powerPresent": power_readings['present_power_reading'][0],
                        "powerMin": power_readings['minimum_power_reading'][0],
                        "powerMax": power_readings['maximum_power_reading'][0]}
        
        return power_result

    def get_host_power_status(self):
        return self.ilo.get_host_power_status()
    
    def get_uptime(self):
        return self.ilo.get_server_power_on_time()

    def power_off(self):
        self.ilo.set_host_power(False)

    def power_on(self):
        self.ilo.set_host_power()

        




