class CocaCola:
    calories    = 140
    sodium      = 45
    total_cab   = 39
    caffeine    = 34
    ingredients = [
        'High Fructose Corn Syrup',
        'Carbonated Water',
        'Natural Flavors',
        'Caramel Color',
        'Caffeine'
    ]
    def _init_(self,logo_name):
        self.local_logo = logo_name
    def drink(self):
        print('You got {} cal energy!'.format(self.calories))
class CaffeineFree(CocaCola):
    caffeine = 0
    ingredients = [
        'High Fructose Corn Syrup',
        'Carbonated Water',
        'Phosphoric Acid',
        'Natural Flavors',
        'Caramel Color',
    ]
coke_a = CaffeineFree('')
coke_a.drink()