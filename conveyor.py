"""Parametric belt conveyor — generated entirely from code with build123d.

Change any parameter below and re-run: frame, rollers, belt, legs, and load
box all update together. No manual CAD editing.
"""
from build123d import *

# ==========================================
# PARAMETERS (mm)
# ==========================================
CONVEYOR_LENGTH = 1000
CONVEYOR_WIDTH = 300
ROLLER_DIAMETER = 60
FRAME_HEIGHT = 80
FRAME_THICKNESS = 5
LEG_HEIGHT = 400

print("Building belt conveyor model...")

# ==========================================
# 1. SIDE FRAMES (steel/aluminum profile)
# ==========================================
with BuildPart() as side_frame_1:
    with BuildSketch(Plane.XZ):
        Rectangle(CONVEYOR_LENGTH, FRAME_HEIGHT)
    extrude(amount=FRAME_THICKNESS)
    side_frame_1 = side_frame_1.part.moved(Location((0, (CONVEYOR_WIDTH / 2) + FRAME_THICKNESS / 2, 0)))

with BuildPart() as side_frame_2:
    with BuildSketch(Plane.XZ):
        Rectangle(CONVEYOR_LENGTH, FRAME_HEIGHT)
    extrude(amount=FRAME_THICKNESS)
    side_frame_2 = side_frame_2.part.moved(Location((0, -(CONVEYOR_WIDTH / 2) - FRAME_THICKNESS / 2, 0)))

# ==========================================
# 2. END ROLLERS (cylindrical drums)
# ==========================================
roller_x_pos = (CONVEYOR_LENGTH / 2) - (ROLLER_DIAMETER / 2)

with BuildPart() as roller_front:
    with BuildSketch(Plane.YZ):
        Circle(radius=ROLLER_DIAMETER / 2)
    extrude(amount=CONVEYOR_WIDTH, both=True)
    roller_front = roller_front.part.moved(Location((roller_x_pos, 0, 0)))

with BuildPart() as roller_back:
    with BuildSketch(Plane.YZ):
        Circle(radius=ROLLER_DIAMETER / 2)
    extrude(amount=CONVEYOR_WIDTH, both=True)
    roller_back = roller_back.part.moved(Location((-roller_x_pos, 0, 0)))

# ==========================================
# 3. BELT
# ==========================================
with BuildPart() as belt:
    with BuildSketch(Plane.XZ):
        # Belt profile as a capsule (slot) wrapping both rollers, 2mm over roller diameter
        SlotOverall(CONVEYOR_LENGTH, ROLLER_DIAMETER + 4)
    extrude(amount=CONVEYOR_WIDTH, both=True)

    # Hollow out the interior where the rollers pass through
    with BuildSketch(Plane.XZ):
        SlotOverall(CONVEYOR_LENGTH, ROLLER_DIAMETER)
    extrude(amount=CONVEYOR_WIDTH + 2, both=True, mode=Mode.SUBTRACT)

# ==========================================
# 4. LEGS (support profiles)
# ==========================================
leg_x_pos = (CONVEYOR_LENGTH / 2) - 100  # inset 100mm from each end

with BuildPart() as legs:
    with BuildSketch(Plane.XY):
        with Locations((leg_x_pos, 0), (-leg_x_pos, 0)):
            Rectangle(40, CONVEYOR_WIDTH + (FRAME_THICKNESS * 2))
    extrude(amount=-LEG_HEIGHT)  # extrude down (-Z) to the floor
    legs = legs.part.moved(Location((0, 0, -FRAME_HEIGHT / 2)))

# ==========================================
# 5. DUMMY LOAD (box riding the belt)
# ==========================================
with BuildPart() as dummy_box:
    with BuildSketch(Plane.XY):
        Rectangle(200, 150)
    extrude(amount=100)
    dummy_z = (ROLLER_DIAMETER / 2) + 2  # roller radius + belt thickness
    dummy_box = dummy_box.part.moved(Location((0, 0, dummy_z)))

# ==========================================
# ASSEMBLY + EXPORT
# ==========================================
sf1, sf2 = side_frame_1, side_frame_2
rf, rb = roller_front, roller_back
blt = belt.part
lg = legs
dummy = dummy_box

sf1.color = Color("DarkSlateGray")
sf2.color = Color("DarkSlateGray")
rf.color = Color("Silver")
rb.color = Color("Silver")
blt.color = Color("Black")
lg.color = Color("DarkSlateGray")
dummy.color = Color("Orange")

assembly = Compound(children=[sf1, sf2, rf, rb, blt, lg, dummy])

if __name__ == "__main__":
    export_step(assembly, "conveyor.step")
    export_stl(assembly, "conveyor.stl")
    print("Saved conveyor.step and conveyor.stl")
