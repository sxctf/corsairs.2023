<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Управление записью</title>
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
        .colortext{
            background-color: black;
            color: forestgreen;
        }

    </style>
</head>
<body>
<table class="menu" border="0px" align="center" width="100%">
    <tbody>
    <tr>
        <td><h2><a href="/" style="color: forestgreen">Main Page</a></h4></td>
        <td><h2><a href="/news" style="color: forestgreen">Ship's log</a></h2></td>
        <td><h2><a href="/private-news" style="color: forestgreen">Add route</a></h2></td>
    </tr>
    </tbody>
</table>

<form action="/checkCode" method="post">
<label>Enter access code</label>
<input type="text" name="verificationCode" class="colortext">
<input type="submit" value="Get access" class="colortext">
</form>

<#if taskSize!=0>
<h2>Task list(task count : ${taskSize})</h2>
<table border="1px">
    <tr>
        <td>Id</td>
        <td>Team ID</td>
        <td>Destination</td>
        <td>Goods description</td>
        <td>Depature date</td>
        <td>Status</td>
        <td>Access code</td>

    </tr>
    <#list taskList as task>
        <tr>
            <td>${task.id}</td>
            <td>${task.name}</td>
            <td>${task.destination}</td>
            <td>${task.description}</td>
            <td>${task.date}</td>
            <td>${task.status}</td>
            <td>${task.accessId}</td>
        </tr>
    </#list>
</table>
</#if>

</body>
</html>