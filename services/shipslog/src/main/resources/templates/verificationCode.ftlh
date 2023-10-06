<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Access Code</title>
    <link rel="stylesheet" type="text/css" href="/style.css">
    <style type="text/css">
        A {
            text-decoration: none;
            color: forestgreen;
        }
        A:hover {
            text-decoration: underline;
            color: yellowgreen;
        }
        table{
            width: 90%;
            border: 1px;
            margin: auto;
        }
        td{
            text-align: center;
        }

    </style>
</head>
<body>
<table class="menu" border="0px" align="center" width="100%">
    <tbody>
    <tr>
        <td><h2><a href="/">Main</a></h2></td>
        <td><h2><a href="/news">Ship's log</a></h2></td>
        <td><h2><a href="/private-news">Add route</a></h4></td>
        <td><h2><a href="/check">Check route</a></h2></td>
    </tr>
    </tbody>
</table>
<#if verificationCode!='0'>
<br>
<h3> Your access code is ${verificationCode}</h3>
<br>
<h3> To save the opportunity to access extended data, we highly recommend you to save your access code in a safe
    place. It's impossible to restore it
</h3>
<#else>
<h3>Data are not avaliable. Workflow is broken, please use menu.</h3>
</#if>
</body>
</html>