
const ctx = document.getElementById('chart1');
  
    var chart1 = new Chart(ctx, {
      type: 'line',
      data: {
        labels: ["No data"],
        datasets: [{
          label: '# of Votes',
          data: [0],
          borderWidth: 1
        }]
      }
    });
    var chart2 = new Chart(document.getElementById('chart2'), {
        type: 'bar',
        data: {
            labels: ["No data"],
            datasets: [{
                label: 'demande',
                data: [0],
                borderColor: 'rgba(200, 99, 132, 1)',
                borderWidth: 2,
                fill: false,
            },
            {
              label: 'Quantité commandé',
              data: [0],
              borderColor: 'rgba(0, 255, 132, 1)',
              borderWidth: 2,
              fill: true,
          }],
        },
        options: {
          scales: {
            y: {
              beginAtZero: true
            }
          }
        }});
    var chart3 = new Chart(document.getElementById('chart3'), {
      type: 'bar',
      data: {
        labels: [0],
        datasets: [{
          label: 'Demande',
          data: ["No data"],
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
    var chart4 = new Chart(document.getElementById('chart4'), {
      type: 'pie',
      data: {
        labels: [0],
        datasets: [{
          label: 'Demande',
          data: ["No data"],
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

     
  function updateData() {
    var productName = document.getElementById('id_product').options[document.getElementById('id_product').selectedIndex].text;
    var scenario = document.getElementById('id_scenario').value;
    var yearName = document.getElementById('year-input').value;

    // Première requête Fetch
    event.preventDefault();
    fetch('/get_product_details/' + productName)
    .then(response => response.json())
    .then(data => {
        if (data.error) {
          alert(data.error);
      } else {
        document.getElementById('product-name').value = data.product_name;
        document.getElementById('qte-unitaire').value = data.qte_unitaire;
        document.getElementById('unit-cost').value = data.unit_cost;
        document.getElementById('fixed-command-cost').value = data.fixed_command_cost;
        document.getElementById('holding-rate').value = data.holding_rate;
        document.getElementById('service-level').value = data.service_level;
        document.getElementById('product-display').textContent = data.product_name;
        document.getElementById('period-display').textContent = "Attendez un instant";
        document.getElementById('command-cost-display').textContent = "Attendez un instant";
        document.getElementById('holding-cost-display').textContent = "Attendez un instant";
        document.getElementById('purchase-cost-display').textContent = "Attendez un instant";
        document.getElementById('total-cost-display').textContent = "Attendez un instant";
        document.getElementById('economic-quantity-display').textContent = "Attendez un instant";
        document.getElementById('without-budget-display').textContent = "Attendez un instant";
      }
        // Deuxième requête Fetch dans la chaîne
        return fetch('/handle_scenario/'+ scenario + "/" + productName + "/" + yearName);
    })
    .then(response => response.json())
  .then(data => {
      // Mise à jour du graphique après que la deuxième requête soit terminée
      chart2.data.labels = data.month;
      chart2.data.datasets[0].data = data.quantité;
      chart2.data.datasets[0].label = "demande " + productName;
      chart2.data.datasets[1].data = data.order;
      chart2.data.datasets[1].label = "quantité commandé " + productName;
      chart2.update();
      chart1.data.labels = data.date;
      chart1.data.datasets[0].data = data.stock_level;
      chart1.data.datasets[0].label = "Stock" + productName;
      chart1.update();
      chart3.data.labels = data.product_names;
      chart3.data.datasets[0].data = data.demand_all_product;
      chart3.update();
      document.getElementById('period-display').textContent = yearName;
      document.getElementById('command-cost-display').textContent = data.command_cost;
      document.getElementById('holding-cost-display').textContent = data.inventory_cost;
      document.getElementById('purchase-cost-display').textContent = data.buying_cost;
      document.getElementById('total-cost-display').textContent = data.total_cost;
      document.getElementById('economic-quantity-display').textContent = data.eoq;
      document.getElementById('without-budget-display').textContent = data.without_budget;
  });
}

document.getElementById('id_product').addEventListener('change', updateData);
document.getElementById('year-input').addEventListener('change', updateData);
document.getElementById('id_scenario').addEventListener('change', updateData);
