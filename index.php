<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Get File</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 0;
            padding: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            height: 45vh;
            background-color: #f4f4f4;
        }

        .card {
            max-width: 350px;
            width: 100%;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }

        .card-header {
            background-color: #3498db;
            color: #fff;
            padding: 15px;
            text-align: center;
        }

        .card-body {
            padding: 20px;
        }

        .download-btn {
            background: #00bf03;
            background-image: -webkit-linear-gradient(top, #00bf03, #008f02);
            background-image: -moz-linear-gradient(top, #00bf03, #008f02);
            background-image: -ms-linear-gradient(top, #00bf03, #008f02);
            background-image: -o-linear-gradient(top, #00bf03, #008f02);
            background-image: linear-gradient(to bottom, #00bf03, #008f02);
            -webkit-border-radius: 3;
            -moz-border-radius: 3;
            border-radius: 3px;
            font-family: Arial;
            color: #ffffff;
            font-size: 18px;
            padding: 10px 50px 10px 50px;
            text-decoration: none;
       }

       .download-btn:hover {
            background: #000000;
            text-decoration: none;
       }
    </style>
</head>
<body>
    <div class="card">
        <div class="card-header">
            File Information
        </div>
        <div class="card-body">
            <?php
            $files = glob('*'); // Get all files in the current directory
            if (!empty($files)) {
                $firstFile = $files[0];
                $fileSize = filesize($firstFile);
                $fileType = mime_content_type($firstFile);
                ?>
                <p><strong>File Name:</strong> <?php echo $firstFile; ?></p>
                <p><strong>File Size:</strong> <?php echo formatBytes($fileSize); ?></p>
                <p><strong>File Type:</strong> <?php echo $fileType; ?></p>
            <?php
            }
            ?>
            <br>
          <center><a href="<?php echo $firstFile; ?>" class="download-btn" download>Download</a></center>
        </div>
    </div>

    <?php
    function formatBytes($bytes, $precision = 2) {
        $units = ['B', 'KB', 'MB', 'GB', 'TB'];

        $bytes = max($bytes, 0);
        $pow = floor(($bytes ? log($bytes) : 0) / log(1024));
        $pow = min($pow, count($units) - 1);

        return number_format($bytes / pow(1024, $pow), $precision) . ' ' . $units[$pow];
    }
    ?>
</body>
</html>
