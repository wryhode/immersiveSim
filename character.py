class Item():
    """Items are everything from tools to body parts"""
    def __init__(self):
        self.parent = None

class BodyPart(Item):
    """Any body part"""
    def __init__(self):
        Item.__init__(self)
        self.name = ""
        self.health = 10

class Nail(BodyPart):
    """Finger nail"""
    def __init__(self):
        BodyPart.__init__(self)
        self.name = "FingerNail"

class Eye(BodyPart):
    """Eye"""
    def __init__(self):
        BodyPart.__init__(self)
        self.name = "Eye"

class Tooth(BodyPart):
    """Tooth"""
    def __init__(self):
        BodyPart.__init__(self)
        self.name = "Tooth"
        self.sharpness = 5

class Tounge(BodyPart):
    """Tounge"""
    def __init__(self):
        BodyPart.__init__(self)
        self.name = "Tounge"

class Finger(BodyPart):
    """Finger"""
    def __init__(self):
        BodyPart.__init__(self)
        self.nail = Nail()
        self.nail.parent = self
        self.name = "Finger"

class Toe(Finger):
    """Toe"""
    def __init__(self):
        Finger.__init__(self)
        self.name = "Toe"

class Hand(BodyPart):
    """Hand with arbitrary amount of fingers"""
    def __init__(self):
        BodyPart.__init__(self)
        self.fingers = {}
        self.name = "Hand"

    def add_finger(self,name):
        self.fingers[name] = Finger()
        self.fingers[name].name = name
        self.fingers[name].parent = self
    
    def init_human_hand(self):
        self.add_finger("thumb")
        self.add_finger("index")
        self.add_finger("middle")
        self.add_finger("ring")
        self.add_finger("pinky")

class Foot(Hand):
    """Basically a hand *But it's a foot!!*"""
    def __init__(self):
        Hand.__init__(self)
        self.toes = {}
        self.name = "Foot"

    def add_toe(self,name):
        self.fingers[name] = Finger()
        self.fingers[name].name = name
        self.fingers[name].parent = self
    
    def init_human_foot(self):
        self.add_finger("big")
        self.add_finger("long")
        self.add_finger("middle")
        self.add_finger("ring")
        self.add_finger("pinky")

class Leg(BodyPart):
    """Humanoid leg"""
    def __init__(self):
        BodyPart.__init__(self)
        self.thigh = BodyPart()
        self.thigh.name = "Thigh"
        self.calf = BodyPart()
        self.calf.name = "Calf"
        self.calf.parent = self.thigh
        self.foot = Foot()
        self.foot.init_human_foot()
        self.foot.parent = self.calf

class Arm(BodyPart):
    """Humanoid arm"""
    def __init__(self):
        BodyPart.__init__(self)
        self.name = "Arm"
        self.upper_arm = BodyPart()
        self.upper_arm.name = "UpperArm"
        self.lower_arm = BodyPart()
        self.lower_arm.name = "LowerArm"
        self.lower_arm.parent = self.upper_arm
        self.hand = Hand()
        self.hand.init_human_hand()
        self.hand.parent = self.lower_arm

class Head(BodyPart):
    """Humanoid head"""
    def __init__(self):
        BodyPart.__init__(self)
        self.name = "Head"
        self.left_eye = Eye()
        self.left_eye.parent = self
        self.right_eye = Eye()
        self.right_eye.parent = self
        self.tounge = Tounge()
        self.tounge.parent = self
        self.teeth = []
        for t in range(32):
            th = Tooth()
            th.parent = self
            self.teeth.append(th)

class Torso(BodyPart):
    """Humanoid torso"""
    def __init__(self):
        BodyPart.__init__(self)
        self.name = "Torso"
        self.left_arm = Arm()
        self.right_arm = Arm()
        self.left_leg = Leg()
        self.right_leg = Leg()
        self.head = Head()