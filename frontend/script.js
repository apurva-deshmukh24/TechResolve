
// Get status CSS class
function getStatusClass(status) {

    return status.toLowerCase();
}


// Update diagnostic status
function updateStatus(elementId, result) {

    const element = document.getElementById(elementId);

    element.textContent = result.status;
    element.className = getStatusClass(result.status);

}


// Run Full Diagnostics
async function runDiagnostics() {

    const button = document.getElementById("run-btn");

    button.disabled = true;
    button.textContent = "Running Diagnostics...";

    try {

        const response = await fetch("/api/diagnostics");

        if (!response.ok) {
            throw new Error("Diagnostic request failed");
        }

        const data = await response.json();


        // Update diagnostic cards
        updateStatus("internet-status", data.internet);
        updateStatus("performance-status", data.performance);
        updateStatus("storage-status", data.storage);
        updateStatus("dns-status", data.dns);


        // Update CPU
        document.getElementById("cpu-value").textContent =
            data.performance.cpu + "%";

        document.getElementById("cpu-bar").style.width =
            data.performance.cpu + "%";


        // Update RAM
        document.getElementById("ram-value").textContent =
            data.performance.ram + "%";

        document.getElementById("ram-bar").style.width =
            data.performance.ram + "%";


        // Update Storage
        document.getElementById("storage-value").textContent =
            data.storage.free_gb + " GB Free";


        // Update Timestamp
        document.getElementById("last-updated").textContent =
            "Last checked: " + data.timestamp;


        // Generate Recommendations
        generateRecommendations(data);


        // Load History
        await loadHistory();

    }

    catch (error) {

        alert("Unable to run diagnostics. Check the backend server.");

        console.error(error);

    }

    finally {

        button.disabled = false;
        button.textContent = "Run Full Diagnostics";

    }

}


// Generate Troubleshooting Recommendations
function generateRecommendations(data) {

    const list = document.getElementById("recommendation-list");

    list.innerHTML = "";

    const recommendations = [];


    // Internet
    if (data.internet.status === "Critical") {

        recommendations.push(
            "Internet connection failed. Check your Wi-Fi or Ethernet connection."
        );

    }


    // CPU
    if (data.performance.cpu >= 75) {

        recommendations.push(
            "High CPU usage detected. Close unnecessary applications and background tasks."
        );

    }


    // RAM
    if (data.performance.ram >= 75) {

        recommendations.push(
            "High RAM usage detected. Close unused applications to free memory."
        );

    }


    // Storage
    if (data.storage.used >= 85) {

        recommendations.push(
            "Storage space is running low. Remove unnecessary files or move them to external storage."
        );

    }


    // DNS
    if (data.dns.status === "Critical") {

        recommendations.push(
            "DNS resolution failed. Check your internet connection and DNS configuration."
        );

    }


    // Healthy System
    if (recommendations.length === 0) {

        recommendations.push(
            "Your system looks healthy. No major issues were detected."
        );

    }


    // Display Recommendations
    recommendations.forEach(message => {

        const item = document.createElement("div");

        item.className = "recommendation-item";

        item.textContent = "✓ " + message;

        list.appendChild(item);

    });

}


// Load Diagnostic History
async function loadHistory() {

    try {

        const response = await fetch("/api/history");

        if (!response.ok) {
            throw new Error("Unable to load history");
        }

        const records = await response.json();

        const historyList = document.getElementById("history-list");

        historyList.innerHTML = "";


        if (records.length === 0) {

            historyList.textContent =
                "No diagnostic history available.";

            return;

        }


        records.forEach(record => {

            const item = document.createElement("div");

            item.className = "history-item";


            const timestamp = document.createElement("p");
            timestamp.textContent = "Date: " + record.timestamp;

            const internet = document.createElement("p");
            internet.textContent =
                "Internet: " + record.internet_status;

            const performance = document.createElement("p");
            performance.textContent =
                "Performance: " + record.performance_status;

            const storage = document.createElement("p");
            storage.textContent =
                "Storage: " + record.storage_status;

            const dns = document.createElement("p");
            dns.textContent =
                "DNS: " + record.dns_status;


            item.append(
                timestamp,
                internet,
                performance,
                storage,
                dns
            );

            historyList.appendChild(item);

        });

    }

    catch (error) {

        console.error("History error:", error);

    }

}


// Load history when page opens
document.addEventListener("DOMContentLoaded", loadHistory);
