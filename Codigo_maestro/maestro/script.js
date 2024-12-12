/** Petición HTTP de la data al maestro. */
async function fetchData() {
    try {
      const response = await fetch("/data");
      const data = await response.json();
      renderData(data);
    } catch (error) {
      console.error("Error al buscar la data:", error);
    }
  }
  
  const ALL_TERMINALS = [
    "TeoriaDelDescontrol",
    "ClubTA",
    "TeamISI",
    "Colapintos",
    "Brogramadores",
    "LosOgata",
    "MonteCarlo",
    "Rompecircuitos",
    "LosFachas",
  ];
  
  /** Renderizar la información disponible de cada equipo en su menu del dashboard. */
  function renderData(data) {
    if (data.terminales_conectados) {
      for (const t of ALL_TERMINALS) {
        // Indicar si está desconectado o no
        const container = document.getElementById(t);
        if (data.terminales_conectados.includes(t)) {
          container.parentElement.classList.remove("disconnected");
          container.parentElement.classList.add("connected");
        } else {
          container.parentElement.classList.add("disconnected");
        }
      }
    }
    if (data.TeoriaDelDescontrol) {
      renderTeoriaDelDescontrol(data.TeoriaDelDescontrol);
    }
    if (data.ClubTA) {
      renderClubTA(data.ClubTA);
    }
    if (data.TeamISI) {
      renderTeamISI(data.TeamISI);
    }
    if (data.Colapintos) {
      renderColapintos(data.Colapintos);
    }
    if (data.Brogramadores) {
      renderBrogramadores(data.Brogramadores);
    }
    if (data.LosOgata) {
      renderLosOgata(data.LosOgata);
    }
    if (data.MonteCarlo) {
      renderMonteCarlo(data.MonteCarlo);
    }
    if (data.Rompecircuitos) {
      renderRompecircuitos(data.Rompecircuitos);
    }
    if (data.LosFachas) {
      renderLosFachas(data.LosFachas);
    }
  }
  
  function renderTeoriaDelDescontrol(data) {
    const container = document.getElementById("TeoriaDelDescontrol");
  
    // Generar el HTML dinámicamente con los datos proporcionados
    container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  }
  
  
  
  
  function renderTeamISI(data) {
    const container = document.getElementById("TeamISI");
   const tableStyle = `
   border-collapse: collapse;
   width: 100%;
   margin-top: 15px;
   font-family: Arial, sans-serif;
  `;
  
  const tdStyle = `
   border: 1px solid #dddddd;
   text-align: center;
   padding: 10px;
   background-color: #f9f9f9;
   color: #333;
  `;
  
  const thStyle = `
   border: 1px solid #dddddd;
   padding: 10px;
   background-color: #ae2ccf;
   color: white;
   text-align: center;
  `;
  
  // Actualizamos el HTML con estilos
  container.innerHTML = `<div
   style="display: flex; gap: 10px; justify-content: center; padding: 10px 0px;"
  >
   
   <div style="width: 55%;">
     <table style="${tableStyle}">
       <tr>
         <th style="${thStyle}">Relay</th>
         <th style="${thStyle}">Angulo Brazo</th>
         <th style="${thStyle}">Posicion panel eje X</th>
         <th style="${thStyle}">Posicion panel eje Y</th>
       </tr>
       <tr>
         <td style="${tdStyle}">${data.Relay}</td>
         <td style="${tdStyle}">${data.Brazo}</td>
         <td style="${tdStyle}">${data.Posicion_panel_eje_x}</td>
         <td style="${tdStyle}">${data.Posicion_panel_eje_y}</td>
         
       </tr>
     </table>
   </div>
  </div>`;
  
  
     //container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  }
    
    
    
  function renderRompecircuitos(data) {
    const container = document.getElementById("Rompecircuitos");
    container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  }
  
  function renderMonteCarlo(data) {
    const container = document.getElementById("MonteCarlo");
    container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  }
  
  function renderLosOgata(data) {
    const container = document.getElementById("LosOgata");
    // Personalizar por el equipo correspondiente
    container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  }
  
  function renderLosFachas(data) {
    const container = document.getElementById("LosFachas");
    container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  }
  
  function renderColapintos(data) {
    const container = document.getElementById("Colapintos");
  
    // Actualizamos el HTML con estilos
    container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  }
  
  function renderClubTA(data) {
    const container = document.getElementById("ClubTA");
    // Personalizar por el equipo correspondiente
    container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  }
  
  function renderBrogramadores(data) {
    const container = document.getElementById("Brogramadores");
    container.innerHTML = `
      <div class="flex flex-col mt-2 bg-white p-4 rounded-lg">
          <p class="voltaje">Voltaje medido: ${data.voltaje}</p>
          <p class="destornilladores">Destornilladores con bajo voltaje: ${data.D_pocoV}</p>
          <p class="destornilladores">Destornilladores con alto voltaje: ${data.D_altoV}</p>
      </div>
    `;
    // Personalizar por el equipo correspondiente
    //container.innerHTML = `<pre>${JSON.stringify(data, null, 2)}</pre>`;
  }
  
  const FETCH_INTERVAL_MS = 500;
  
  // Buscar data nueva cada cierto intervalo
  setInterval(fetchData, FETCH_INTERVAL_MS);
  
  