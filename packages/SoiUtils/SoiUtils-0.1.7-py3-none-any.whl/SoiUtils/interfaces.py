import abc

class Resetable(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        return hasattr(__subclass,'reset') and callable(__subclass.reset) or NotImplemented
    
    @abc.abstractmethod
    def reset(self, *args,**kwargs) -> None:
        """reset the object"""
        raise NotImplementedError

 
class Updatable(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, __subclass: type) -> bool:
        return hasattr(__subclass,'update') and callable(__subclass.update) or NotImplemented
    

    @abc.abstractmethod 
    def update(*args,**kwargs) -> None:
        # update the object according to a new configuration
        raise NotImplementedError
        
    

    
