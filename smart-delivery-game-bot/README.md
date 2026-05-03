# AI Delivery Routing Simulation

A browser-based delivery routing simulator built with HTML, CSS, and vanilla JavaScript.

## Features
- 15x15 grid with obstacles
- Warehouse + multiple delivery orders
- Priority-based decision making
- A* pathfinding
- Animated bot movement
- Persistent colored route visualization

## Scoring Logic
\[
\text{Score} = (\text{priority} \times 10) - (\text{distance} \times 2)
\]

## AI Algorithm Used

The simulator uses a **hybrid AI approach**:

1. **A\* Pathfinding (local shortest path)**  
	For any two points (current bot position and an order), A\* computes the shortest valid path while avoiding blocked cells.

2. **Greedy Priority-Distance Selection (global decision step-by-step)**  
	At each delivery step, the bot evaluates every remaining order using:

	\[
		ext{Score} = (\text{priority} \times 10) - (\text{distance} \times 2)
	\]

	- `priority`: user-assigned importance of the order
	- `distance`: A\* path length from current position to that order

3. **Iterative Routing**  
	The bot selects the order with the highest score, moves there, marks it delivered, then repeats until all orders are completed.

### Why this works
- A\* ensures obstacle-aware shortest movement between nodes.
- The score balances urgency (priority) and travel cost (distance).
- Greedy re-evaluation after every delivery adapts decisions to the bot’s new location.

## Files
- `index.html` – app structure
- `styles.css` – UI styling
- `script.js` – simulation logic

## Run
Open `index.html` in any modern browser.
