messages = None
characters = None

class Item(object):
	def __init__(self,display="??",xPosition=0,yPosition=0):
		self.display = display
		self.xPosition = xPosition
		self.yPosition = yPosition
		self.listeners = []
		self.walkable = False
		self.room = None
		self.name = "item"

	def apply(self,character):
		messages.append("i can't do anything useful with this")

	def changed(self):
		messages.append(self.name+": Object changed")
		for listener in self.listeners:
			listener()

	def addListener(self,listenFunction):
		if not listenFunction in self.listeners:
			self.listeners.append(listenFunction)

	def delListener(self,listenFunction):
		if listenFunction in self.listeners:
			self.listeners.remove(listenFunction)

class Corpse(Item):
	def __init__(self,xPosition=0,yPosition=0,name="corpse"):
		super().__init__("࿊ ",xPosition,yPosition)
		self.walkable = True

class Hutch(Item):
	def __init__(self,xPosition=0,yPosition=0,name="Hutch",activated=False):
		self.activated = activated
		if self.activated:
			super().__init__("ꙭ ",xPosition,yPosition)
		else:
			super().__init__("Ѻ ",xPosition,yPosition)

	def apply(self,character):
		if not self.activated:
			self.activated = True
			self.display = "ꙭ "
		else:
			self.activated = False
			self.display = "Ѻ "

class Lever(Item):
	def __init__(self,xPosition=0,yPosition=0,name="lever",activated=False):
		self.activated = activated
		self.display = {True:" /",False:" |"}
		self.name = name
		super().__init__(" |",xPosition,yPosition)
		self.activateAction = None
		self.deactivateAction = None
		self.walkable = True

	def apply(self,character):
		if not self.activated:
			self.activated = True
			self.display = " /"
			messages.append(self.name+": activated!")

			if self.activateAction:
				self.activateAction(self)
		else:
			self.activated = False
			self.display = " |"
			messages.append(self.name+": deactivated!")

			if self.deactivateAction:
				self.activateAction(self)
		self.changed()

class Furnace(Item):
	def __init__(self,xPosition=0,yPosition=0,name="Furnace"):
		self.name = name
		self.activated = False
		super().__init__("ΩΩ",xPosition,yPosition)

	def apply(self,character):
		messages.append("Furnace used")
		foundItem = None
		for item in character.inventory:
			try:
				canBurn = item.canBurn
			except:
				continue
			if not canBurn:
				continue

			foundItem = item

		if not foundItem:
			messages.append("keine KOHLE zum anfeuern")
		else:
			self.activated = True
			self.display = "ϴϴ"
			character.inventory.remove(foundItem)
			messages.append("burn it ALL")
		self.changed()

class Display(Item):
	def __init__(self,xPosition=0,yPosition=0,name="Display"):
		self.name = name
		super().__init__("۞ ",xPosition,yPosition)

class Wall(Item):
	def __init__(self,xPosition=0,yPosition=0,name="Wall"):
		self.name = name
		super().__init__("⛝ ",xPosition,yPosition)

class Pipe(Item):
	def __init__(self,xPosition=0,yPosition=0,name="Wall"):
		self.name = name
		super().__init__("✠✠",xPosition,yPosition)

class Coal(Item):
	def __init__(self,xPosition=0,yPosition=0,name="Coal"):
		self.name = name
		self.canBurn = True
		super().__init__(" *",xPosition,yPosition)
		self.walkable = True

class Door(Item):
	def __init__(self,xPosition=0,yPosition=0,name="Door"):
		super().__init__("⛒ ",xPosition,yPosition)
		self.name = name
		self.walkable = False
		self.display = '⛒ '

	def apply(self,character):
		if self.walkable:
			self.close()
		else:
			self.open()
	
	def open(self):
		self.walkable = True
		self.display = '⭘ '
		self.room.open = True

	def close(self):
		self.walkable = False
		self.display = '⛒ '
		self.room.open = False

class Pile(Item):
	def __init__(self,xPosition=0,yPosition=0,name="pile",itemType=Coal):
		self.name = name
		self.canBurn = True
		self.type = itemType
		super().__init__("ӫӫ",xPosition,yPosition)

	def apply(self,character):
		messages.append("Pile used")
		character.inventory.append(self.type())
		character.changed()

class Acid(Item):
	def __init__(self,xPosition=0,yPosition=0,name="pile",itemType=Coal):
		self.name = name
		self.canBurn = True
		self.type = itemType
		super().__init__("♒♒",xPosition,yPosition)

	def apply(self,character):
		messages.append("Pile used")
		character.inventory.append(self.type())
		character.changed()
