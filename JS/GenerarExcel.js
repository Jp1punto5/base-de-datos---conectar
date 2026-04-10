function descargarExcel() {
  console.log("SheetJS version:", XLSX.version);

  const tablaHTML = document.getElementById("tabla");

  if (!tablaHTML) {
    console.error("No se encontró la tabla con id 'tabla'");
    mostrarAlerta("La tabla aún no ha sido generada.","warning");
    return;
  }

  try {
    const filas = Array.from(tablaHTML.rows);

    const datos = filas.map((fila, rowIndex) => {
      const celdas = Array.from(fila.cells);

      return celdas.map((cell) => {
        const texto = cell.textContent?.trim() || "";
        const aTag = cell.querySelector('a');

        // 🔗 HIPERVÍNCULO
        if (aTag && aTag.href) {
          return {
            v: aTag.textContent?.trim() || "Ver mapa",
            l: { Target: aTag.href },
            s: {
              font: { color: { rgb: "0563C1" }, underline: true }
            }
          };
        }

        // 📍 DETECCIÓN AUTOMÁTICA DE COORDENADAS (PRO 🔥)
        const match = texto.match(/^(-?\d+\.\d+),\s*(-?\d+\.\d+)$/);
        if (match) {
          const lat = match[1];
          const lon = match[2];

          return {
            v: texto,
            l: { Target: `https://www.google.com/maps?q=${lat},${lon}` },
            s: {
              font: { color: { rgb: "0563C1" }, underline: true }
            }
          };
        }

        //📅 DETECTAR FECHA CON HORA
        if (esFechaConHora(texto))
        {
            const fecha = convertirAFechaExcel(texto);

            return  {
                        v: fecha,
                        t: "d",
                        z: "dd/mm/yyyy hh:mm:ss" // con hora

                    };
        }

        // 📅 FECHA SIN HORA
        if (esFechaSinHora(texto))
        {
            const fecha = convertirAFechaExcel(texto);

            return {
                    v: fecha,
                    t:"d",
                    z:"dd/mm/yyyy" // sin hora
            }
        }



        // 🔢 Detectar números largos (IMEI, SIMCARD, etc)
        if (!isNaN(texto) && texto !== "") {

        // 👉 Si es muy largo, tratar como texto
        if (texto.length >= 10) {
            return {
            v: texto,
            t: "s"
            };
        }

        // 👉 números normales (edad, cantidad, etc)
        return Number(texto);
        }

        return texto;
      });
    });

    const wb = XLSX.utils.book_new();
    const ws = XLSX.utils.aoa_to_sheet(datos);

    // 🎨 ESTILO ENCABEZADO (fila 1)
    const range = XLSX.utils.decode_range(ws['!ref']);
    for (let col = range.s.c; col <= range.e.c; col++) {
      const cellRef = XLSX.utils.encode_cell({ r: 0, c: col });
      if (ws[cellRef]) {
        ws[cellRef].s = {
          font: { bold: true },
          alignment: { horizontal: "center" }
        };
      }
    }

    // 📏 AUTO ANCHO DE COLUMNAS (PRO 🔥)
    const colWidths = datos[0].map((_, colIndex) => {
      let maxLength = 10;

      datos.forEach(row => {
        const val = row[colIndex];
        const length = val?.v ? val.v.length : val?.toString().length;
        if (length > maxLength) maxLength = length;
      });

      return { wch: maxLength + 2 };
    });

    ws['!cols'] = colWidths;

    XLSX.utils.book_append_sheet(wb, ws, tabla);

    XLSX.writeFile(wb, `Modulo_${tabla}.xlsx`);

    console.log("archivo descargado..");

  } catch (error) {
    console.error("Error al generar el Excel:", error);
    mostrarAlerta("Hubo un problema al generar el archivo Excel.","error");
  }
}



function esFechaConHora(texto) {
  return /^\d{2}-\d{2}-\d{4} \d{2}:\d{2}:\d{2}$/.test(texto);
}

function esFechaSinHora(texto) {
  return /^\d{2}-\d{2}-\d{4}$/.test(texto);
}

function convertirAFechaExcel(texto) {
  const [fecha, hora] = texto.split(" ");

  const [dia, mes, anio] = fecha.split("-");
  const [h = 0, m = 0, s = 0] = (hora || "").split(":");

  return new Date(Date.UTC(anio, mes - 1, dia, h, m, s));
}