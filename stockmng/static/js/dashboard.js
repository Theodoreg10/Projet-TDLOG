
const ctx = document.getElementById('chart1');
  
    var chart1 = new Chart(ctx, {
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
            labels: ["No data"],
            datasets: [{
                label: 'demand',
                data: [0],
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

    document.getElementById('id_product').addEventListener('change', function() {
      var productName = this.options[this.selectedIndex].text;
  
      // Première requête Fetch
      fetch('/get_product_details/' + productName)
      .then(response => response.json())
      .then(data => {
          document.getElementById('product-name').value = data.product_name;
          document.getElementById('qte-unitaire').value = data.qte_unitaire;
          document.getElementById('unit-cost').value = data.unit_cost;
          document.getElementById('fixed-command-cost').value = data.fixed_command_cost;
          document.getElementById('holding-rate').value = data.holding_rate;
          document.getElementById('service-level').value = data.service_level;
  
          // Deuxième requête Fetch dans la chaîne
          return fetch('/handle_scenario1/' + productName);
      })
      .then(response => response.json())
      .then(data => {
          // Mise à jour du graphique après que la deuxième requête soit terminée
          chart2.data.labels = data.date;
          chart2.data.datasets[0].data = data.quantité;
          chart2.data.datasets[0].label = "quantité " + productName;
          chart2.update();
      });
  });

$(document).ready(function() {
  // Définir les références aux éléments HTML
  var scenarioSelect = $('#scenario-selection-form select');
  var productSelect = $('#product-selection-form select');

  // Gérer le changement de scénario ou de produit
  $('#scenario-selection-form').on('change', 'select', function() {
      // Récupérer les valeurs sélectionnées
      var selectedScenario = scenarioSelect.val();

      // Effectuer une requête Ajax vers votre backend Django
      $.ajax({
          url: 'handle_scenario1',  // Remplacez par l'URL de votre vue Django
          method: 'GET',
          data: {
              scenario: selectedScenario,
              product: selectedProduct
          },
          success: function(data) {
              // Mettre à jour le graphique avec les nouvelles données
              updateChart(myChart, data);
          },
          error: function(error) {
              console.log('Erreur lors de la récupération des données :', error);
          }
      });
  });

  // Fonction pour mettre à jour le graphique avec les nouvelles données
  function updateChart(chart, newData) {
      // Assurez-vous d'adapter cela en fonction de votre configuration de graphique spécifique
      myChart.data.labels = newData["date"];
      myChart.data.datasets[0].data = newData["quantité"];
      chart.data = newData;
      chart.update();
  }
});

