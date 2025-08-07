<?php
// --- CONFIGURATION ---
$csv_file = 'news-month.csv';
$default_start_date = date('Y-m-d', strtotime('-7 days'));
$default_end_date = date('Y-m-d');

// --- PHP LOGIC: READ AND FILTER DATA ---

// Get dates from form submission, or use defaults
$start_date_str = $_GET['start_date'] ?? $default_start_date;
$end_date_str = $_GET['end_date'] ?? $default_end_date;

$news_articles = [];

// Check if the CSV file exists
if (file_exists($csv_file)) {
    // Open the CSV file for reading
    if (($handle = fopen($csv_file, "r")) !== FALSE) {
        $header = fgetcsv($handle, 1000, ","); // Read and discard the header

        while (($data = fgetcsv($handle, 1000, ",")) !== FALSE) {
            // Assuming CSV columns are: วันที่ของข่าว, ประเภทข่าว, แหล่งที่มา, ข่าว
            $article_date_str = date('Y-m-d', strtotime($data[0]));

            $article_date = new DateTime($article_date_str);
            $start_date = new DateTime($start_date_str);
            $end_date = new DateTime($end_date_str);

            // Filter by date range
            if ($article_date >= $start_date && $article_date <= $end_date) {
                $news_articles[] = [
                    'date' => $data[0],
                    'category' => $data[1],
                    'source' => $data[2],
                    'title' => $data[3]
                ];
            }
        }
        fclose($handle);
    }
}
?>
<!DOCTYPE html>
<html lang="th">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Thai Economic News</title>
    <style>
        /* --- CSS STYLING --- */
        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            background-color: #f4f7f6;
            color: #333;
            margin: 0;
            padding: 20px;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
            border-bottom: 2px solid #e0e0e0;
            padding-bottom: 20px;
        }

        h1 {
            color: #2c3e50;
        }

        /* Form Styling */
        .filter-form {
            background-color: #ffffff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
            margin-bottom: 30px;
            display: flex;
            flex-wrap: wrap;
            gap: 20px;
            align-items: center;
            justify-content: center;
        }

        .filter-form label {
            font-weight: bold;
        }

        .filter-form input[type="date"] {
            padding: 8px;
            border: 1px solid #ccc;
            border-radius: 4px;
            font-size: 16px;
        }

        .filter-form button {
            padding: 10px 20px;
            background-color: #3498db;
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            cursor: pointer;
            transition: background-color 0.3s;
        }

        .filter-form button:hover {
            background-color: #2980b9;
        }

        /* News Grid Styling */
        .news-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 20px;
        }

        .news-card {
            background-color: #ffffff;
            border: 1px solid #e0e0e0;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
            display: flex;
            flex-direction: column;
        }

        .news-card h3 {
            margin-top: 0;
            color: #2c3e50;
        }

        .news-card .meta {
            font-size: 0.9em;
            color: #7f8c8d;
            margin-top: auto; /* Pushes meta to the bottom */
            padding-top: 10px;
        }

        .no-news {
            background-color: #fff;
            padding: 40px;
            text-align: center;
            border-radius: 8px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.05);
        }

        /* Responsive Design */
        @media (max-width: 768px) {
            body {
                padding: 10px;
            }
            .filter-form {
                flex-direction: column;
                align-items: stretch;
            }
        }
    </style>
</head>
<body>

    <div class="container">
        <header>
            <h1>Thai Economic News Viewer</h1>
        </header>

        <!-- Date Filter Form -->
        <form action="index.php" method="GET" class="filter-form">
            <div>
                <label for="start_date">Start Date:</label>
                <input type="date" id="start_date" name="start_date" value="<?php echo htmlspecialchars($start_date_str); ?>">
            </div>
            <div>
                <label for="end_date">End Date:</label>
                <input type="date" id="end_date" name="end_date" value="<?php echo htmlspecialchars($end_date_str); ?>">
            </div>
            <button type="submit">Filter News</button>
        </form>

        <!-- News Display Grid -->
        <main class="news-grid">
            <?php if (!empty($news_articles)): ?>
                <?php foreach ($news_articles as $article): ?>
                    <div class="news-card">
                        <h3><?php echo htmlspecialchars($article['title']); ?></h3>
                        <div class="meta">
                            <strong>Date:</strong> <?php echo htmlspecialchars(date('d M Y', strtotime($article['date']))); ?><br>
                            <strong>Source:</strong> <?php echo htmlspecialchars($article['source']); ?>
                        </div>
                    </div>
                <?php endforeach; ?>
            <?php else: ?>
                <div class="no-news">
                    <h2>No news found for the selected period.</h2>
                    <p>Please try adjusting the date range or make sure the <code><?php echo $csv_file; ?></code> file contains relevant data.</p>
                </div>
            <?php endif; ?>
        </main>
    </div>

</body>
</html>
