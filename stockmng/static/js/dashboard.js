document.getElementById('id_product').addEventListener('change', function() {
    var productName = this.options[this.selectedIndex].text;
    fetch('/get_product_details/' + productName)
    .then(response => response.json())
    .then(data => {
        document.getElementById('product-name').value = data.product_name;
        document.getElementById('qte-unitaire').value = data.qte_unitaire;
        document.getElementById('unit-cost').value = data.unit_cost;
        document.getElementById('fixed-command-cost').value = data.fixed_command_cost;
        document.getElementById('holding-rate').value = data.holding_rate;
        document.getElementById('service-level').value = data.service_level;
    });
});

var select = document.querySelector("#scenario-selection-form select");

select.onchange = function() {
    // Code to be executed when the selected option changes
    var selectedOption = this.options[this.selectedIndex].value;
    console.log("Selected option: " + selectedOption);
    
};


const ctx = document.getElementById('chart1');
  
    new Chart(ctx, {
      type: 'bar',
      data: {
        labels: ['Red', 'Blue', 'Yellow', 'Green', 'Purple', 'Orange'],
        datasets: [{
          label: '# of Votes',
          data: [12, 19, 3, 5, 2, 3],
          borderWidth: 1
        }]
      },
      options: {
        scales: {
          y: {
            beginAtZero: true
          }
        }
      }
    });
    var chart2 = new Chart(document.getElementById('chart2'), {
        type: 'line',
        data: {
            labels: ['Label1', 'Label2', 'Label3', 'Label4', 'Label5'],
            datasets: [{
                label: 'Chart 2',
                data: [5, 15, 25, 35, 45],
                borderColor: 'rgba(255, 99, 132, 1)',
                borderWidth: 2,
                fill: false,
            }],
        },
        options: {
            scales: {
                x: {
                    grid: {
                        display: false,
                    },
                },
                y: {
                    grid: {
                        display: false,
                    },
                }
            }
    }});
