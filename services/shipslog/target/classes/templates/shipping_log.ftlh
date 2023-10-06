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
        .colortext{
            background-color: black;
            color: forestgreen;
        }

    </style>
</head>
<body>
<table class="menu" >
    <tbody>
    <tr>
        <td><h2><a href="/">Main</a></h2></td>
        <td><h2><a href="/news">Ship's log</a></h4></td>
        <td><h2><a href="/check">Check route</a></h2></td>
    </tr>
    </tbody>
</table>
<br>
<h1>Ship's log</h1>
<h3>Add route</h3>

<form action="/add" method="post">
    <table border="1px">
        <tr>
            <td>
                <label>Team ID</label>
                <input type="text" name="name" class="colortext">
            </td>
            <td>
                <label>Destination</label>
                <input type="text" name="destination" class="colortext">
            </td>
            <td>
                <label>Goods description</label>
                <input type="text" name="description" class="colortext">
            </td>
            <td>
                <label>Depature date</label>
                <input type="date" name="date" class="colortext">
            </td>
            <td>
                <label>Status</label>
                <br>
                <input type="radio" name="status" value = "Planned" align="left"> Plan </input>
                <br>
                <input type="radio" name="status" value = "Successful" align="left"> Sussess </input>
                <br>
                <input type="radio" name="status" value = "Failed" align="left"> Fail </input>
            </td>

            <td>
                <input type="submit" value="Add" class="colortext">
            </td>

        </tr>

    </table>
</form>

<br>
<h2>Depatures (Total : ${taskSize})</h2>
<table border="1px">
    <tr>
        <td>Team ID</td>
        <td>Destination</td>
        <td>Date</td>
        <td>Status</td>
    </tr>
    <#list taskList as task>
    <tr>
        <td>${task.name}</td>
        <td>${task.destination}</td>
        <td>${task.date}</td>
        <td>${task.status}</td>
    </tr>
</#list>
</table>

</body>
</html>