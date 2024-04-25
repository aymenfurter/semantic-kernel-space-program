from semantic_kernel.functions.kernel_function_decorator import kernel_function

class SpaceProgramPlugin:
    """
    Description: This plugin provides functions to interact with a space program.

    Usage:
        kernel.add_plugin(SpaceProgramPlugin(), plugin_name="space_program_plugin")

    Examples:
        space_program_plugin.listLaunchSite()
        space_program_plugin.selectLaunchSite("Guiana Space Centre, French Guiana")
        space_program_plugin.buySpaceRocket("Falcon Heavy")
        space_program_plugin.launchRocket()
    """

    def __init__(self):
        self.selected_launch_site = None
        self.selected_rocket = None
        self.estimated_cost = None
        self.selected_suit = None
        self.food_supplies = None
        self.fuel_type = None
        self.fuel_quantity = None

    @kernel_function(name="ListLaunchSites", description="Lists available launch sites")
    def listLaunchSite(self):
        return [
            "Guiana Space Centre, French Guiana",
            "Baikonur Cosmodrome, Kazakhstan",
            "Vandenberg Space Force Base, USA",
            "Rocket Lab Launch Complex 1, New Zealand",
            "Cape Canaveral Space Launch Complex, Florida"
        ]

    @kernel_function(name="SelectLaunchSite", description="Selects a launch site")
    def selectLaunchSite(self, site: str):
        self.selected_launch_site = site
        return f"Launch site set to: {site}"

    @kernel_function(name="ListSpacesuits", description="Lists available spacesuits")
    def listSpacesuit(self):
        return [
            "EMU (Extravehicular Mobility Unit)",
            "ACES (Advanced Crew Escape Suit)",
            "Sokol Space Suit",
            "Orlan Space Suit",
            "Launch Entry Suit"
        ]

    @kernel_function(name="ListSpaceRockets", description="Lists available space rockets")
    def listSpaceRocket(self):
        return [
            "Falcon 9",
            "Falcon Heavy",
            "Starship",
            "SLS (Space Launch System)",
            "Delta IV Heavy",
            "Ariane 5",
            "Soyuz",
            "Atlas V",
            "New Glenn",
            "Vulcan Centaur"
        ]

    @kernel_function(name="BuyFuel", description="Buys fuel for the rocket based on type")
    def buyFuel(self, fuel_type: str, quantity: int):
        """
        Buys a specific type of fuel and the quantity for the rocket.

        Args:
        fuel_type (str): The type of fuel, e.g., 'RP-1', 'Liquid Hydrogen', 'Hydrazine'.
        quantity (int): The quantity in kilograms.

        Returns:
        str: Confirmation message of the fuel purchase.
        """
        self.fuel_type = fuel_type
        self.fuel_quantity = quantity
        print(f"{quantity} kg of {fuel_type} fuel purchased.")
        return f"{quantity} kg of {fuel_type} fuel purchased."

    @kernel_function(name="BuyFood", description="Buys food supplies for the mission, comma seperated, provide exact meal names and make sure to keep morale high")
    def buyFood(self, meals: str):
        """
        Buys a list of meals for the mission.

        Args:
        meals (comma seperated): List containing the names of meals.

        Returns:
        str: Confirmation message of the food purchase.
        """
        self.food_supplies = meals
        print(f"Food supplies purchased: {meals}")
        return f"Food supplies purchased: {meals}"

    @kernel_function(name="BuySpaceRocket", description="Selects a space rocket based on name")
    def buySpaceRocket(self, rocket: str):
        self.selected_rocket = rocket
        print(f"Rocket selected: {rocket}")
        return f"Rocket selected: {rocket}"

    @kernel_function(name="SetEstimatedCosts", description="Sets the estimated costs for the mission")
    def setEstimatedCosts(self, cost: str):
        self.estimated_cost = cost
        print(f"Estimated costs set to: {cost}")
        return f"Estimated costs set to: {cost}"

    @kernel_function(name="BuySpacesuit", description="Selects a spacesuit based on name")
    def buySpacesuit(self, name: str):
        self.selected_suit = name
        print(f"Spacesuit color selected: {name}")
        return f"Spacesuit color selected: {name}"

    @kernel_function(name="LaunchRocket", description="Launches the selected rocket if all conditions are met. Make sure to have selected a launch site, rocket, estimated costs, spacesuit, food supplies, and fuel.")
    def launchRocket(self):
        if self.selected_launch_site is None:
            print("Error: Launch site has not been selected.")
            return "Try again. Error: Launch site has not been selected."
        if self.selected_rocket is None:
            print("Error: Rocket has not been selected.")
            return "Try again. Error: Rocket has not been selected."
        if self.estimated_cost is None:
            print("Warning: Estimated costs have not been set.")
        if self.selected_suit is None:
            print("Error: Spacesuit has not been selected.")
            return "Try again. Error: Spacesuit has not been selected."
        if self.food_supplies is None:
            print("Error: Food supplies have not been purchased.")
            return "Try again. Error: Food supplies have not been purchased."
        if self.fuel_type is None or self.fuel_quantity is None:
            print("Error: Fuel has not been purchased.")
            return "Try again. Error: Fuel has not been purchased."

        print(f"Launching {self.selected_rocket} from {self.selected_launch_site} with estimated costs of {self.estimated_cost}.")
        return f"MISSION COMPLETED: Launching {self.selected_rocket} from {self.selected_launch_site} with estimated costs of {self.estimated_cost}."