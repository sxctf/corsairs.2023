<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Ship's log</title>
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
<table class="menu">
    <tbody>
    <tr>
        <td><h2><a href="/">Main</a></h2></td>
        <td><h2><a href="/private-news">Add route</a></h2></td>
        <td><h2><a href="/check">Check route</a></h2></td>
    </tr>
    </tbody>
</table>
<h1>Ship's log</h1>

<br>
<h2>Depatures (total : ${taskSize})</h2>
<table border="1px">
    <tr>
        <td>ID</td>
        <td>Team ID</td>
        <td>Destination</td>
        <td>Date</td>
        <td>Status</td>
    </tr>
    <#list taskList as task>
        <tr>
            <td>${task.id}</td>
            <td>${task.name}</td>
            <td>${task.destination}</td>
            <td>${task.date}</td>
            <td>${task.status}</td>
        </tr>
    </#list>
</table>
</body>
</html>