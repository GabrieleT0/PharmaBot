class UserInfo:
    def __init__(self,email = None,password = None,firstName = None,lastName = None,medicine = None):
        self.email = email
        self.password = password
        self.firstName = firstName
        self.lastName = lastName
        self.medicine = medicine

    def get_user_info(self):
        return f"{self.email} {self.firstName} {self.lastName} {self.medicine}"
    
    def get_medicine(self):
        if isinstance(self.medicine,list):
            if len(self.medicine) > 0:
                medicineLi = []
                for medicine in self.medicine:
                    name = medicine['name']
                    type = medicine['type']
                    grams = medicine['grams']
                    expirationDate = medicine['expirationDate']
                    if type is None:
                        type = ''
                    if grams is None:
                        grams = ''
                    medicine_str = f"{name} {type} {grams} Data scadenza: {expirationDate}"
                    medicineLi.append(medicine_str.strip())
                return medicineLi
            else:
                return False
        else:
            return False
