var charts = {};

	function createGraph(chartName, chartType, chartObj) {
		var ctx = document.getElementById(chartName);
		var legendDisplay = false;
		var gridLinesDisplay = true;
		if (chartType == 'pie') {
			legendDisplay = true;
			gridLinesDisplay = false;
		}
        var colours = chartObj.data.datasets[0].backgroundColor;
        if (chartType == 'line') {
            colours = '#8DB600'
        }

		var chart = new Chart(ctx, {
			type: chartType,
			data: {
				labels: chartObj.data.labels,
				datasets: [{
					label: chartObj.data.datasets[0].label,
					data: chartObj.data.datasets[0].data,
					backgroundColor: colours
				}]
			},
			options: {
				legend: {
					display: legendDisplay
				},
				scales: {
					yAxes: [{
						ticks: {
							beginAtZero: true,
							display: gridLinesDisplay

						},
						gridLines: {
							display: gridLinesDisplay
						}
					}]
				}
			}
		});

		return chart;
	}

	function openTab(evt, tabName, chartName, chartObj) {
		var i, tabcontent, tablinks;
		tabcontent = document.getElementsByClassName("tabcontent");
		for (i = 0; i < tabcontent.length; i++) {
			tabcontent[i].style.display = "none";
		}
		tablinks = document.getElementsByClassName("tablinks");
		for (i = 0; i < tablinks.length; i++) {
			tablinks[i].className = tablinks[i].className.replace(" active", "");
		}
		document.getElementById(tabName).style.display = "block";
		evt.currentTarget.className += " active";

		<!-- charts -->
		if (typeof charts[chartName] != "undefined") {
			charts[chartName].destroy();
		}
		var chartType = chartObj.type;
		charts[chartName] = createGraph(chartName, chartType, chartObj);
	}

	function changeGraph(evt, chartName, chartType, chartObj) {
		charts[chartName].destroy();
		charts[chartName] = createGraph(chartName, chartType, chartObj);
	}