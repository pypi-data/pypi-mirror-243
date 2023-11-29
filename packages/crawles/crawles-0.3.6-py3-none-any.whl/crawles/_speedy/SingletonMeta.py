class SingletonMeta(type):
    def __call__(cls, *args, **kwargs):
        """单例模式"""
        if not hasattr(cls, '_instance'):
            cls._instance = super(SingletonMeta, cls).__call__(*args, **kwargs)
        return cls._instance



