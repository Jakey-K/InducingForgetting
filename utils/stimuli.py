import pandas as pd

################### CUES & TARGETS #########################
def loadWordPairs():
    cues = [
        "Galaxy",      # 1.  glasses with a crack
        "Umbrella",    # 2.  2 cars crashed into eachother
        "Calculator",  # 3.  bridge surrounded by foliage
        "Bread",       # 4.  fat machine gun thing
        "Harmony",     # 5.  bomb explosion cloud thing 
        "Coconut",     # 6.  dog getting teeth inspected
        "Compass",     # 7.  some army on a ship downing another ship
        "Jupiter",     # 8.  kkk setting a massive cross on fire
        "Bicycle",     # 9.  2 dudes boxing 
        "Pyramid",     # 10. 2 dogs fighting surrounded by a crowd
        "Violin",      # 11. demolished house next to an intact one
        "Camera",      # 12. wolf bearing it's teeth 
        "Lemonade",    # 13. creepy school classroom with upside-down chair
        "Pillow",      # 14. child wielding a hand gun
        "Banana",      # 15. 5 blood-like straight vertical marks on a wall like a claw
        "Jazz",        # 16. knife on a sheet with blood on it and the sheet 
        "Cactus",      # 17. line of dead pigs(?) hanging upside-down
        "Marathon",    # 18. child crying (white, male, sweater, coat)
        "Sapphire",    # 19. dead guy hanging off a bridge with crowd below 
        "Satellite",   # 20. man holding a woman's hair and shoving a gun in her face
        "Volcano",     # 21. 6 raspberries close-up
        "Moxie",       # 22. motorway photo timelapse, red one side white one side
        "Pepper",      # 23. graveyard on sand and closest one is wood, rest is stone
        "Mirror",      # 24. staple & 2 buttons forming a sad face 
        "Parachute",   # 25. 2 seals fighting? barking at eachother?
        "Teapot",      # 26. woman and daughter walk past a street covered by garbage with face masks on
        "Telescope",   # 27. mouse in-front of a cat and looks paralyzed in fear
        "Sandwich",    # 28. bridge? on fire, very large fire
        "Raincoat",    # 29. young overweight boy, visibly irritated, undergoes dental inspection
        "Saxophone",   # 30. some analog horror photo person with their mouth open
        "Kangaroo",    # 31. logs forming a boat with hands stretched out from the bottom of the photo
        "Puzzle",      # 32. guy on the floor, bloodied, visibly in pain, in boxing ring with crowd
        "Lighthouse",  # 33. dude lying in a ditch covered in red sand and 4 chinese? soldiers surrounding him
        "Carpet",      # 34. sports car, crashed, mid-air, with crowd around fleeing for their lives
        "Whistle",     # 35. soldier crouched, inspecting 2 boxes of skeletons
        "Eagle",       # 36. abstract painting of 3 creepy skeletons
        "Calendar",    # 37. woman lying on floor, od'd on pills and drooling
        "Strawberry",  # 38. 2 doctors carrying a severely wounded woman 
        "Volleyball",  # 39. guy robbing? a woman with a knife to her neck
        "Rainbow",     # 40. baby sheep? under a rock surrounded by 2 dead crows?
        "Microscope",  # 41. man with back to graveyard and a man in the distance
        "Suitcase",    # 42. 2 guys breaking into a house, one beating a window with a sowrd and one chucking a baseball bat 
        "Dictionary",  # 43. massive rubber duck in lake
        "Chameleon",   # 44. police dog attacking a man
        "Hammock",     # 45. teddy bear on some train tracks looking down
        "Paperclip",   # 46. puppy being pulled by a collar 
        "Melody",      # 47. woman with no pupils appearing to bite into a rose
        "Toothbrush",  # 48. guy crouched over and is on fire, being beaten? by a guy with a bat
        "Meadow",      # 49. young child running from a soldier with a gun
        "Anchor",      # 50. back part of commercial airplane crashed into house
        "Chocolate",   # 51. mass amount of garbage on ocean shore
        "Sailboat",    # 52. soldiers running on a snowy terrain
        "Snowflake",   # 53. hand gun with bullets lying around it
        "Ladder",      # 54. 4 guys break into silver car, wielding baseball bats
        "Oxygen",      # 55. inmate held by a guy with knife to his neck with 2 people at inmates' feet wrapped in blankets?
        "Whirlpool",   # 56. window with a persons' hands coming out of it
        "Windmill",    # 57. person adminstering an injection into their arm
        "Bottle",      # 58. line of disabled people all wearing crutches
        "Mushroom",    # 59. woman holding onto a shirtless man, begging?, whilst man whips? her
        "Crayon",      # 60. man digging a site with dead woman in a pit, plenty of blood around the pit
        "Globe",       # 61. crowd running from a building in a city appearing to have been blown up
        "Dragonfly",   # 62. masked man on bed with many big guns around
        "Eclipse",     # 63. top-down photo of cockroach, pure white background
        "Sunflower",   # 64. orange in a persons hand, carved angry face
        "Quartz",      # 65. many red & white candles dimly lighting a room
        "Screwdriver", # 66. 2 people with gas masks inside a bus
        "Peppermint",  # 67. girl, by herself, operating some white factory machine
        "Feather",     # 68. village levelled by earthquake, rubble everywhere
        "Trampoline",  # 69. black suv crashed into a fence outside of a house
        "Quack",       # 70. some ferret-like animal bearing teeth at the camera
        "Rhinoceros",  # 71. lots of people putting their hands on some asian politician-looking guys face
        "Marble",      # 72. soldiers invading house, guy in closet with child
        "Giraffe",     # 73. guy, face covered, standing infront of a van on fire
        "Blender",     # 74. soldiers' gun pointed to photoshopped child
        "Oasis",       # 75. lots of people, hands cuffed, put up against a wall by soldiers with guns
        "Zeppelin",    # 76. abstract fat horror creature
        "Pancake",     # 77. close-up of spider with long legs upside-down
        "Harpoon",     # 78. 3 alcoholics on bench, 1 passed out, 1 crying
        "Wax",         # 79. fox standing over a dead cows(>) head
        "Blossom",     # 80. dead guy lying on his stomach on the ground, and some guy is taking a photo of him 
        "Lantern",     # 81. an orange bike in a garage
        "Thunder",     # 82. a sign "Millesime Bio" with the EU flag, France flag and ? flag on top
        "Rocket",      # 83. 2 cables, one white, one orange, both wrapped circularly, not UK plugs
        "Helmet",      # 84. 2 old rustic sofas in front of a table, on top if its mugs, book, newspaper
        "Candle",      # 85. a backpack with WD40 in the pocket and a water bottle next to it
        "Pickaxe",     # 86. an ice cream sundae with a cherry on top
        "Tunnel",      # 87. a panda hugging onto a tree branch
        "Temple",      # 88. a moose in a green field hill outlined by the light
        "Scissors",    # 89. shirtless light skin man, visibly frustrated, attempting to open a jar of dill pickles
        "Shovel",      # 90. white staircase in, presumably, a country side with a child standing on top of it
        "Trophy",      # 91. knife, presumably a flip knife, appearing to be wedged into a table
        "Crown",       # 92. 2 black pigs lying next to eachother on hay
        "Chainsaw",    # 93. 3-4 men running on a road, bright red light behind them
        "Firework",    # 94. kitten, visibly scared, looking at what is presumably a bernese mountain dog
        "Robot",       # 95. light skin man holds up a white snake, mouth open, with one hand on the snakes neck
        "Bucket",      # 96. odd circular statue with a creepy face carved into it
        "Mask",        # 97. a football in the middle of a stadium, alone
        "Toaster",     # 98. a lion in the middle of a green area, lying down
        "Meteor",      # 99. 4 people riding horses, 2 have crsahed into eachother, both people falling off 
        "Cradle",      # 100. big ship riding in the water, presumably storming and raining
        "Igloo",       # 101. a woman in a grocery store putting something in her pocket, presumably shoplifting
        "Magnet",      # 102. an ape in what is presumably a shower stall, sucking his thumb?, sort of sitting and curled up into the corner
        "Pencil",      # 103. 2 men, naked, pinned on a wall, hands up, with a man holding a gun near the camera
        "Balloon",     # 104. light skin woman, wearing white, on the floor, blood on arm and chest
        "Tornado",     # 105. light skin woman, lying on a bed, visibly very skinny, looks exasperated
        "Canyon",      # 106. old light skin man, visibly upset, sitting next to a white (hospital?) bed, old white woman in bed
        "Spectrum",    # 107. dark skin woman, visbly upset, wiping face (tears?) with a towel, sitting next to what appears to be a wrapped body
        "Vortex",      # 108. a train that has fallen over, many people near and on it
        "Siren",       # 109. woman, visibly confused, is looking at a person near the camera who has a gun, environment is like a typical house
        "Locket",      # 110. 2 Chinese? police officers, with batons, stand behind a young boy in white, who has his hands tied up with chains up on the the wall
    ]

    numbers = list(range(1, 111))
    targets = [f"{num}.jpg" for num in numbers]
    types = ["think"] * 20 + ["nothink"] * 20 + ["baseline"] * 20 + ["filler"] * 20 + ["bystander"] * 30

    data = {
        "cue": cues,
        "target": targets,
        "type": types
    }

    wordPairs = pd.DataFrame(data)
    return wordPairs
