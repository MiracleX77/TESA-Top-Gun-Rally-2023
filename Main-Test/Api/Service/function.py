class FunctionService:

    @staticmethod
    def setStatus(water_height:float):
        if water_height > 120:
            return "DANGER"
        elif water_height > 110:
            return "WARNING"
        else:
            return "NORMAL"
    