<html>
<head>
<title>Victimco</title>
<style>

body,input {
    font-family: "Trebuchet MS", Arial, sans-serif;
}
body {
    background-color: #FFEFEF;
    margin:0;
}

div.notice {
    width 100%;
    background-color: black;
    border-bottom: 4px solid red;
    color: white;
    padding: 10px;
    margin: 0 0 20px 0;
    text-align: center;
}

div.container {
    width: 900px;
    margin: 10px auto 10px auto;
    border: 1px solid black;
    background-color: #fff;
    box-shadow: 0px 0px 20px rgba(100,100,100,1);
    zbox-shadow: 0px 0px 5px rgba(100,100,100,0.4);
}

div.header {
    width: 100%;
    margin: 0;
    background-color: #C05757;
    text-align: center;
    border-bottom: 1px solid black;
}

div.content {
    padding: 15px;
    background-color: white;
}

pre {
    margin: 20px;
    padding: 10px;
    background-color: #ccc;
}
</style>
</head>
<body>
<div class=notice>This is a sample web application for Duke University ECE590-03 "Computer and Information Security". Maintained by <a style="color: #FCA;" href="mailto:Tyler DOT Bletsch AT duke.edu">Tyler Bletsch</a>.</div>
<div class=container>
    <div class=header><img src="logo.png"></div>
    <div class=content>
        <h1>Welcome!</h1>
        Here at Victimco, we are an committed to providing top shelf internet services, including domain registration and SSL certificates. We beat the competition on price because we code very fast and don't waste time on testing and auditing.
        <p>
        Would you like to register a domain with us? Type a domain below to see if it's registered already. Our premiere service uses a Trustico-inspired domain <i>whois</i> to pull up info on your desired domain!
        <!-- HINT: Trustico's shame: https://www.bankinfosecurity.com/trustico-shuts-down-website-after-possible-flaw-a-10692 -->

        <!-- Golden ticket #1: TRUSTICO'S SHAMEFUL SECRET -->
        <!-- ^^ added 2018-10-31. sorry this ticket wasn't in place from the start -->
        <form method="post">
        <input type=text name=domain placeholder="example.com" style="width: 20em;">
        <input type=submit value="Check it!">
        
        <?php
            if ($_POST['domain']) {
                echo "<pre>".shell_exec("whois -H " . $_POST['domain'] . " 2>/dev/null")."</pre>";
            }
        ?>
    </div>
</div>
</body>
</html>
