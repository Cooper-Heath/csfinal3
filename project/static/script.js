fetch("/static/pixels.json")
  .then(response => response.json())
  .then(data => {
    const grid = document.getElementById("image-grid");
    const height = data.length;
    const width = data[0].length;


    grid.style.display = "grid";
    grid.style.gridTemplateColumns = `repeat(${width}, 20px)`;
    grid.style.gap = "1px";

    let mouseDown = false;


    window.addEventListener("mousedown", () => { mouseDown = true; });
    window.addEventListener("mouseup", () => { mouseDown = false; });

    data.forEach(row => {
      row.forEach(pixel => {
        const div = document.createElement("div");
        div.className = "pixel-box";
        div.dataset.color = `rgb(${pixel.rgb[0]}, ${pixel.rgb[1]}, ${pixel.rgb[2]})`;

        // Reveal color function
        function reveal() {
          div.style.backgroundColor = div.dataset.color;
          div.classList.add("revealed");
        }

        div.addEventListener("mousedown", reveal);
        div.addEventListener("mouseover", () => {
          if (mouseDown) {
            reveal();
          }
        });

        grid.appendChild(div);
      });
    });
  })
  .catch(err => console.error("Error loading pixels.json:", err));
