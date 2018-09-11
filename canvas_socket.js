
$(function () {
    var dps = [];
    var chart = new CanvasJS.Chart("chartContainer", {
        title: {
            text: "CowNection"
        },
        axisY: {
            includeZero: false
        },
        data: [{
            type: "line",
            dataPoints: dps
        }]
    });

    var xVal = 0;
    var yVal = 100;
    var updateInterval = 1000;
    var dataLength = 20;
    var socket = io();
    $('form').submit(function () {
        socket.emit('chat message', $('#m').val());
        $('#m').val('');
        return false;
    });
    socket.on('chat message', function (msg) {
        dps.push({
            x: xVal,
            y: parseInt(msg)
        });
        xVal++;
    });
    var updateChart = function (count) {

        count = count || 1;
        if (dps.length > dataLength) {
            dps.shift();
        }

        chart.render();
    };

    updateChart(dataLength);
    setInterval(function () { updateChart() }, updateInterval);
});
