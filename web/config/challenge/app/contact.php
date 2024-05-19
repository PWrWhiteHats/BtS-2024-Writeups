<!DOCTYPE html>

<html>
    <head>
        <title>Conf1gurex</title>

        <link rel="stylesheet" type="text/css" href="assets/style.css">
    </head>

    <body>
        <?php

        # Handle form submission
        function upload() {
            if ($_SERVER['REQUEST_METHOD'] === 'POST') {
                $email = $_POST['email'];
                $message = $_POST['message'];
                $file = $_FILES['file'];

                # TODO: Send email with message and file url

                # Check fields
                if (empty($email) || empty($message) || empty($file)) {
                    echo 'All fields are required!';
                    return;
                }

                # Check file size (under 100KB)
                if ($file['size'] > 100000) {
                    echo 'File size too large! Maximum size is 100KB.';
                    return;
                }

                # Check file extension
                $allowed = array('png', 'jpg');
                $filename = $file['name'];
                $ext = explode(".", $filename)[1];
                if (!in_array($ext, $allowed)) {
                    echo 'Invalid file type! Only .png and .jpg files are allowed.';
                    return;
                }

                # Upload file
                $file_path = 'uploads/' . $file['name'];
                move_uploaded_file($file['tmp_name'], $file_path);

                echo '<div style="width: 100%;text-align: center;">Success! <a href="uploads/' . $file['name'] . '">View file</a></div>';
            }
        }

        upload();
        ?>
        <div id="main_wrapper">
            <div id="title">
                <h1>Contact</h1>
            </div>

            <div>
                <form action="contact.php" method="post" enctype="multipart/form-data">
                    <label for="email">Email:</label><br>
                    <input type="email" id="email" name="email"><br><br>
                    <label for="message">Message:</label><br>
                    <textarea id="message" name="message" rows="4" cols="50"></textarea><br><br>
                    <label for="file">Attachment (.png, .jpg allowed):</label><br>
                    <input type="file" id="file" name="file"><br><br>
                    <input class="button" style="background-color: #28b588" type="submit" value="Submit">
                </form>
            </div>

            <div id="buttons">
                <div class="button" onclick="window.location.href = '/'">Back</div>
            </div>

            <footer>
                <p>&copy; 2077 Conf1gurex</p>
            </footer>
        </div>
    </body>
</html>
