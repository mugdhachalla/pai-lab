// ==================== CONSTANTS ====================
const GRID_SIZE = 15;
const GRID_WIDTH = GRID_SIZE;
const GRID_HEIGHT = GRID_SIZE;
const OBSTACLE_PROBABILITY = 0.15;

// ==================== STATE ====================
let grid = [];
let warehouse = null;
let orders = [];
let currentPriority = 5;
let isRunning = false;
let animationSpeed = 300;

// Game state
let currentPosition = null;
let visitedOrders = [];
let currentPath = [];
let traversedPath = [];
let totalDistance = 0;
let totalScore = 0;
let routeSequence = [];

let gameTime = 60; // seconds
let timeLeft = gameTime;
let gameInterval = null;
let dynamicOrderInterval = null;

let gameRunning = false;
let orderExpiryTime = 20; // seconds per order

function startGameTimer() {
    gameRunning = true;
    timeLeft = gameTime;

    gameInterval = setInterval(() => {
        timeLeft--;
        document.getElementById("timeLeft").textContent = timeLeft;

        if (timeLeft <= 0) {
            endGame();
        }
    }, 1000);
}

function startDynamicOrders() {
    stopDynamicOrders();

    dynamicOrderInterval = setInterval(() => {
        if (!gameRunning) return;
        if (!warehouse) return;

        const maxAttempts = 50;
        let attempts = 0;

        while (attempts < maxAttempts) {
            const x = Math.floor(Math.random() * GRID_WIDTH);
            const y = Math.floor(Math.random() * GRID_HEIGHT);
            const cell = grid[y][x];
            const isWarehouse = warehouse.x === x && warehouse.y === y;
            const isDuplicate = orders.some(order => order.x === x && order.y === y);

            if (!cell.isObstacle && !isWarehouse && !isDuplicate) {
                orders.push({
                    id: Date.now(),
                    x: x,
                    y: y,
                    priority: Math.floor(Math.random() * 10) + 1,
                    reward: 50,
                    createdAt: Date.now()
                });

                updateOrdersList();
                renderGrid();
                updateModeInfo(`New dynamic order added at (${x}, ${y}).`);
                break;
            }

            attempts++;
        }
    }, 5000);
}

function stopDynamicOrders() {
    if (dynamicOrderInterval) {
        clearInterval(dynamicOrderInterval);
        dynamicOrderInterval = null;
    }
}
// ==================== GRID INITIALIZATION ====================

/**
 * Creates and initializes the game grid with obstacles
 */
function createGrid() {
    grid = [];
    for (let y = 0; y < GRID_HEIGHT; y++) {
        let row = [];
        for (let x = 0; x < GRID_WIDTH; x++) {
            // Create obstacles randomly, but not in corners
            let isObstacle = Math.random() < OBSTACLE_PROBABILITY &&
                !(x < 2 && y < 2) && !(x >= GRID_WIDTH - 2 && y < 2);
            
            row.push({
                x: x,
                y: y,
                isObstacle: isObstacle,
                isWarehouse: false
            });
        }
        grid.push(row);
    }
}

/**
 * Renders the grid in the HTML
 */
function renderGrid() {
    const container = document.getElementById('gridContainer');
    container.innerHTML = '';
    container.style.display = 'inline-grid';
    container.style.gridTemplateColumns = `repeat(${GRID_WIDTH}, 1fr)`;
    container.style.gap = '0';

    for (let y = 0; y < GRID_HEIGHT; y++) {
        for (let x = 0; x < GRID_WIDTH; x++) {
            const cell = grid[y][x];
            const cellElement = document.createElement('div');
            cellElement.className = 'grid-cell';
            cellElement.id = `cell-${x}-${y}`;

            // Apply styling based on cell type
            if (cell.isObstacle) {
                cellElement.classList.add('obstacle');
            } else if (cell.isWarehouse) {
                cellElement.classList.add('warehouse');
                cellElement.textContent = '📦';
            } else {
                // Check if this cell has an order
                const order = orders.find(o => o.x === x && o.y === y);
                if (order) {
                    cellElement.classList.add('order');
                    if (visitedOrders.includes(order.id)) {
                        cellElement.classList.add('visited');
                    }
                    cellElement.textContent = order.priority;
                }
            }

            // Highlight path (current segment + all previously traversed cells)
            const isCurrentPathCell = currentPath.some(p => p.x === x && p.y === y);
            const isTraversedPathCell = traversedPath.some(p => p.x === x && p.y === y);
            if (isCurrentPathCell || isTraversedPathCell) {
                if (!cell.isWarehouse && !orders.find(o => o.x === x && o.y === y)) {
                    cellElement.classList.add('path');
                }
            }

            // Highlight current position
            if (currentPosition && currentPosition.x === x && currentPosition.y === y) {
                cellElement.classList.add('bot');
                cellElement.textContent = '🤖';
            }

            cellElement.addEventListener('click', () => handleCellClick(x, y));
            container.appendChild(cellElement);
        }
    }
}

/**
 * Adds a grid position to traversed path only once
 */
function addToTraversedPath(position) {
    if (!position) return;
    const exists = traversedPath.some(p => p.x === position.x && p.y === position.y);
    if (!exists) {
        traversedPath.push({ x: position.x, y: position.y });
    }
}

// ==================== CELL INTERACTION ====================

/**
 * Handles cell click for setting warehouse or adding orders
 */
function handleCellClick(x, y) {
    if (isRunning) return;

    const cell = grid[y][x];
    if (cell.isObstacle) {
        alert('Cannot select obstacle cell');
        return;
    }

    // If no warehouse, first click sets it
    if (!warehouse) {
        warehouse = { x, y };
        cell.isWarehouse = true;
        updateModeInfo(`Warehouse set at (${x}, ${y}). Now add orders by clicking on cells.`);
        renderGrid();
    } else if (warehouse.x === x && warehouse.y === y) {
        // Clicking warehouse again removes it
        warehouse = null;
        cell.isWarehouse = false;
        updateModeInfo('Warehouse removed. Click to set a new warehouse.');
        renderGrid();
    } else {
        // Check if already an order at this location
        const existingOrder = orders.find(o => o.x === x && o.y === y);
        if (existingOrder) {
            // Remove order
            orders = orders.filter(o => o.id !== existingOrder.id);
            updateModeInfo(`Order removed from (${x}, ${y})`);
        } else {
            // Add new order
            const priority = parseInt(document.getElementById('priorityInput').value) || 5;
            const orderId = Date.now() + Math.random();
            orders.push({
                id: orderId,
                x: x,
                y: y,
                priority: priority,
                reward: priority * 20,
                createdAt: Date.now()
            });
            updateModeInfo(`Order added at (${x}, ${y}) with priority ${priority}`);
        }
        updateOrdersList();
        renderGrid();
    }
}

// ==================== A* PATHFINDING ====================

/**
 * Heuristic function for A* (Manhattan distance)
 */
function heuristic(a, b) {
    return Math.abs(a.x - b.x) + Math.abs(a.y - b.y);
}

/**
 * A* pathfinding algorithm
 * Finds shortest path from start to end, avoiding obstacles
 */
function aStar(start, end) {
    if (!start || !end) return [];

    const openSet = [start];
    const cameFrom = new Map();
    const gScore = new Map();
    const fScore = new Map();

    const key = (p) => `${p.x},${p.y}`;
    const getValue = (map, p, defaultVal) => {
        const k = key(p);
        return map.has(k) ? map.get(k) : defaultVal;
    };
    const setValue = (map, p, val) => map.set(key(p), val);

    setValue(gScore, start, 0);
    setValue(fScore, start, heuristic(start, end));

    while (openSet.length > 0) {
        // Find node in openSet with lowest fScore
        let current = openSet[0];
        let currentIdx = 0;
        for (let i = 1; i < openSet.length; i++) {
            if (getValue(fScore, openSet[i], Infinity) < getValue(fScore, current, Infinity)) {
                current = openSet[i];
                currentIdx = i;
            }
        }

        if (current.x === end.x && current.y === end.y) {
            // Reconstruct path
            let path = [current];
            while (cameFrom.has(key(current))) {
                current = cameFrom.get(key(current));
                path.unshift(current);
            }
            return path;
        }

        openSet.splice(currentIdx, 1);

        // Check all neighbors (4-directional movement)
        const neighbors = [
            { x: current.x + 1, y: current.y },
            { x: current.x - 1, y: current.y },
            { x: current.x, y: current.y + 1 },
            { x: current.x, y: current.y - 1 }
        ];

        for (const neighbor of neighbors) {
            // Check bounds and obstacles
            if (neighbor.x < 0 || neighbor.x >= GRID_WIDTH ||
                neighbor.y < 0 || neighbor.y >= GRID_HEIGHT ||
                grid[neighbor.y][neighbor.x].isObstacle) {
                continue;
            }

            const tentativeGScore = getValue(gScore, current, Infinity) + 1;
            const neighborGScore = getValue(gScore, neighbor, Infinity);

            if (tentativeGScore < neighborGScore) {
                cameFrom.set(key(neighbor), current);
                setValue(gScore, neighbor, tentativeGScore);
                setValue(fScore, neighbor, tentativeGScore + heuristic(neighbor, end));

                if (!openSet.some(p => p.x === neighbor.x && p.y === neighbor.y)) {
                    openSet.push(neighbor);
                }
            }
        }
    }

    // No path found
    return [];
}

// ==================== SCORING AND DECISION MAKING ====================

/**
 * Calculates score for an order based on reward, travel time, and expiry
 */
function calculateScore(order, position) {
    const path = aStar(position, { x: order.x, y: order.y });

    if (path.length === 0) {
        return { score: -Infinity, distance: Infinity, path: [] };
    }

    const distance = path.length - 1;

    // time penalty (simulate delay)
    const timePenalty = distance;

    // expiry penalty
    const age = (Date.now() - order.createdAt) / 1000;
    const expiryPenalty = age > orderExpiryTime ? 50 : 0;

    const score = order.reward - timePenalty * 2 - expiryPenalty;

    return { score, distance, path };
}

/**
 * Chooses the next best order to deliver based on scoring function
 */
function chooseNextOrder(position) {
    let bestOrder = null;
    let bestScore = -Infinity;
    let bestInfo = null;

    for (const order of orders) {
        // Skip already visited orders
        if (visitedOrders.includes(order.id)) continue;

        const info = calculateScore(order, position);
        if (info.score > bestScore) {
            bestScore = info.score;
            bestOrder = order;
            bestInfo = info;
        }
    }

    return { order: bestOrder, score: bestScore, distance: bestInfo?.distance || 0, path: bestInfo?.path || [] };
}
function endGame() {
    clearInterval(gameInterval);
    stopDynamicOrders();
    gameRunning = false;

    updateModeInfo(`⛔ Game Over! Final Score: ${totalScore}`);
}
// ==================== GAME LOOP ====================

/**
 * Runs the delivery game loop
 */
async function runGame() {
    if (!warehouse || orders.length === 0) {
        alert('Please set a warehouse and add at least one order');
        return;
    }

    isRunning = true;
    document.getElementById('startBtn').disabled = true;
    document.getElementById('resetBtn').disabled = true;
    document.getElementById('randomBtn').disabled = true;

    currentPosition = { x: warehouse.x, y: warehouse.y };
    visitedOrders = [];
    currentPath = [];
    traversedPath = [];
    totalDistance = 0;
    totalScore = 0;
    routeSequence = [];
    updateUI(0);
    updateOrdersList();
    updateRouteOrder();
    updateModeInfo('🎮 Game started! Deliver all orders before time runs out.');

    startGameTimer();
    startDynamicOrders();

    while (gameRunning && visitedOrders.length < orders.length) {
        const { order, score, distance, path } = chooseNextOrder(currentPosition);

        if (!order) {
            console.error('No valid order found');
            break;
        }

        routeSequence.push(order);
        currentPath = path;
        totalDistance += distance;
        totalScore += score;

        for (let i = 1; i < path.length; i++) {
            addToTraversedPath(currentPosition);
            currentPosition = path[i];
            updateUI(visitedOrders.length);
            renderGrid();
            await sleep(animationSpeed);

            if (!gameRunning) return;
        }

        addToTraversedPath(currentPosition);

        visitedOrders.push(order.id);
        updateUI(visitedOrders.length);
        updateOrdersList();
        updateRouteOrder();
        renderGrid();
    }

    updateModeInfo('✅ Game complete! All orders delivered.');
    document.getElementById('startBtn').disabled = false;
    document.getElementById('resetBtn').disabled = false;
    document.getElementById('randomBtn').disabled = false;
    isRunning = false;
}

/**
 * Sleep utility for animation delays
 */
function sleep(ms) {
    return new Promise(resolve => setTimeout(resolve, ms));
}

// ==================== UI UPDATES ====================

/**
 * Updates the mode information display
 */
function updateModeInfo(message) {
    document.getElementById('modeText').textContent = message;
}

/**
 * Updates all UI elements with current statistics
 */
function updateUI(stepCount) {
    document.getElementById('totalDistance').textContent = totalDistance;
    document.getElementById('totalScore').textContent = totalScore.toFixed(1);
    document.getElementById('ordersDelivered').textContent = `${visitedOrders.length} / ${orders.length}`;
    document.getElementById('currentStep').textContent = stepCount;
}

/**
 * Updates the orders list display
 */
function updateOrdersList() {
    const list = document.getElementById('ordersList');
    if (orders.length === 0) {
        list.innerHTML = '<div style="color: #999; font-style: italic;">No orders added yet</div>';
        return;
    }

    list.innerHTML = orders.map(order => `
        <div class="order-item ${visitedOrders.includes(order.id) ? 'visited' : ''}">
            <span>Order at (${order.x}, ${order.y})</span>
            <span class="order-priority">P${order.priority}</span>
        </div>
    `).join('');
}

/**
 * Updates the route order display
 */
function updateRouteOrder() {
    const list = document.getElementById('routeOrder');
    if (routeSequence.length === 0) {
        list.innerHTML = '<div style="color: #999; font-style: italic;">Route will be shown after game starts</div>';
        return;
    }

    list.innerHTML = routeSequence.map((order, index) => `
        <div class="order-item">
            <span><strong>#${index + 1}:</strong> (${order.x}, ${order.y})</span>
            <span class="order-priority">P${order.priority}</span>
        </div>
    `).join('');
}

// ==================== BUTTON HANDLERS ====================

/**
 * Resets the entire game
 */
function reset() {
    warehouse = null;
    orders = [];
    visitedOrders = [];
    currentPosition = null;
    currentPath = [];
    traversedPath = [];
    totalDistance = 0;
    totalScore = 0;
    routeSequence = [];
    isRunning = false;
    clearInterval(gameInterval);
    stopDynamicOrders();
    gameRunning = false;

    createGrid();
    renderGrid();
    updateUI(0);
    updateOrdersList();
    document.getElementById('routeOrder').innerHTML = '<div style="color: #999; font-style: italic;">Route will be shown after game starts</div>';
    updateModeInfo('Grid reset. Click on grid cells to set warehouse (red) or add orders (teal).');

    document.getElementById('startBtn').disabled = false;
    document.getElementById('resetBtn').disabled = false;
    document.getElementById('randomBtn').disabled = false;
}

/**
 * Generates random orders on the grid
 */
function generateRandomOrders() {
    if (!warehouse) {
        alert('Please set a warehouse first');
        return;
    }

    // Clear existing orders
    orders = [];
    visitedOrders = [];

    // Generate 5-8 random orders
    const orderCount = 5 + Math.floor(Math.random() * 4);
    let added = 0;

    while (added < orderCount) {
        const x = Math.floor(Math.random() * GRID_WIDTH);
        const y = Math.floor(Math.random() * GRID_HEIGHT);

        const cell = grid[y][x];
        const isWarehouse = warehouse.x === x && warehouse.y === y;
        const isDuplicate = orders.some(o => o.x === x && o.y === y);
        const isObstacle = cell.isObstacle;

        if (!isWarehouse && !isDuplicate && !isObstacle) {
            const priority = 1 + Math.floor(Math.random() * 10);
            orders.push({
                id: Date.now() + Math.random() + added,
                x: x,
                y: y,
                priority: priority,
                reward: priority * 20,
                createdAt: Date.now()
            });
            added++;
        }
    }

    updateOrdersList();
    renderGrid();
    updateModeInfo(`Generated ${orderCount} random orders. Click "Start Game" to begin.`);
}

// ==================== EVENT LISTENERS ====================

document.getElementById('startBtn').addEventListener('click', runGame);
document.getElementById('resetBtn').addEventListener('click', reset);
document.getElementById('randomBtn').addEventListener('click', generateRandomOrders);

document.getElementById('speedSlider').addEventListener('change', (e) => {
    animationSpeed = parseInt(e.target.value);
    document.getElementById('speedValue').textContent = animationSpeed + 'ms';
});

document.getElementById('priorityInput').addEventListener('change', (e) => {
    currentPriority = parseInt(e.target.value) || 5;
});

// ==================== INITIALIZATION ====================

createGrid();
renderGrid();
updateUI(0);
updateModeInfo('👋 Welcome! Click on grid cells to set warehouse (red) or add orders (teal).');
