

TPS = 5 # Update game (tick; move snake) at this rate

# Settings
INIT_SETTINGS = {
    "grid_size_x": 20,
    "grid_size_y": 14,
}

INIT_PLAYER_X: int = INIT_SETTINGS["grid_size_x"] // 2
INIT_PLAYER_Y: int = INIT_SETTINGS["grid_size_y"] // 2
INIT_LENGTH: int = 5


# Structs Setup
SNAKE_TEXTURE_PACK = "snake"
FOOD_TEXTURE_PACK = "food"
HOTSPOT_TEXTURE_PACK = "hotSpots"
