class Food:
    def __init__(self, name, cost):
        self.name = name
        self.cost = cost
    def getName(self):
        return self.name
    #RETURN COST OF INGREDIENT
    def getCost(self):
        return self.cost
class Recipe:
    def __init__(self, name):
        self.name = name
        self.foodList = [x.lower() for x in self.foodList]
        self.total = 0
    #ADDS FOOD TO RECIPE
    def addFood(self, foodToAdd):
        if foodToAdd not in self.foodList:
            self.foodList.append(foodToAdd.name)
            self.total += foodToAdd.cost
    #CHECKS IF FOOD IS IN RECIPE ALREADY
    def checkFood(self, foodToRemove):
        if foodToRemove in self.foodList:
            self.foodList.remove(foodToRemove.name)
            self.total -= foodToRemove.cost
    #RETURNS COST
    def getRecipeCost(self):
        return self.total
    #DISPLAYS RECIPE
    def formatRecipe(self):
        print("The name is: "+ self.name)
        print("The ingredients are: " + self.foodList)
        print("The total is: " + self.total)
#ADD TO RECIPE LIST
recipeList = []
foodAvailable = []
recipeNum = {}
#GET NEW INGREDIENTS
def getIngredient():
    print("What is the name of the Ingredient?")
    nameOfIngredient = input()
    print("What is the cost?")
    foodCost = input()
    foodCost= int(foodCost)
    #CHECK INPUT
    try:
        myNewFood = Food(nameOfIngredient,foodCost)
        foodAvailable.append(myNewFood)
        return(myNewFood)
    except:
        print("Your input was wrong, try again")
        getIngredient()
#GET RECIPE AND ADD TO DICTIONARY
def getRecipe(num):
    print("What is the name of the recipe?")
    nameOfRecipe = input()
    myNewRecipe = Recipe(nameOfRecipe)
    def AddIngredientsToRecipe():
        print("What is the ingredient?")
        foodString = input()
        print("What is the cost?")
        foodCost = int(input())
        newIngredient = Food(foodString,foodCost)
        myNewRecipe.addFood(newIngredient)
        myNewRecipe.checkFood(newIngredient)
        recipeNum[num] = myNewRecipe
        print("Would you like to add another?(0 for yes or enter for no)")
        option = input()
        option=int(option)
        if (option == 0):
            AddIngredientsToRecipe()
        else:
            return
    AddIngredientsToRecipe()
    #ASK TO PUT MORE RECIPES
    def addRecipe():
        print("Would you like to add another recipe or go back?(0) or (1)")
        newOption = int(input())
        try:
            if newOption == 0:
                getRecipe(num)
            elif newOption==1:
                return
        except:
            print("You have chosen a bad option")
            return
    addRecipe()
#CHECK WHETHER TO ADD RECIPE OR INGREDIENT
def addRecipeOrIngredient():
    while True:
        print("Do you want to enter a recipe or ingredient?")
        recipeOrIngredient = input().lower()
        totalNumRecipes = len(recipeNum)
        try:
            if recipeOrIngredient == "recipe":
                getRecipe(totalNumRecipes)
            if recipeOrIngredient == "ingredient":
                getIngredient()
        except:
            print("Invalid input")
            break
#FORMAT AND DISPLAY RECIPE
def displayRecipe():
    print("Which recipe would you like to display? You must enter the number between 0 and: " + str(len(recipeNum)-1))
    recipeNum1 = input()
    recipeNum1 = int(recipeNum1)
    recipeItem = recipeNum.get(recipeNum1)
    recipeItem.formatRecipe()
#MAIN FUNCTION
if __name__ == "__main__":
    while True:    
        print("Welcome to creating and storing your recipes:")
        print("Would you like to enter a recipe or ingredient or display an existing one?(0 or 1)")
        DisplayOrEnter = input()
        DisplayOrEnter = int(DisplayOrEnter)
        if (DisplayOrEnter == 0):
            addRecipeOrIngredient()
        elif(DisplayOrEnter == 1):
            if (len(recipeNum)==0):
                print("NO RECIPES")
                pass
            else:
                displayRecipe()
        else:
            print("Invalid response")



        
    
