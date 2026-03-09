# Vacuum Cleaner World - All 8 States

locations = ['A', 'B']
status = ['Clean', 'Dirty']

state_number = 1

for vacuum in locations:
    for roomA in status:
        for roomB in status:
            print("State", state_number)
            print("Vacuum Location:", vacuum)
            print("Room A:", roomA)
            print("Room B:", roomB)
            
            if vacuum == 'A' and roomA == 'Dirty':
                print("Action: Suck (Clean Room A)")
            elif vacuum == 'B' and roomB == 'Dirty':
                print("Action: Suck (Clean Room B)")
            elif vacuum == 'A':
                print("Action: Move Right")
            else:
                print("Action: Move Left")
            
            print("-----------------------")
            state_number += 1
