function create_player(player, my_id) {
    output_html = "";

    var mode;

    if ("deduction_pts" in player) {
        mode = 3;
    } else if ("moving_pts" in player) {
        mode = 2;
    } else {
        mode = 1;
    }

    if (mode == 1) {
        output_html += '<svg height="170" width="80">';
    } else if (mode == 2) {
        output_html += '<svg height="190" width="80">';
    } else {
        output_html += '<svg height="215" width="80">';
    }

    if (player.id == my_id) {
        output_html += '<text x="50%" y="28" text-anchor="middle" fill="black" font-size="20" font-weight="bold">YOU</text>';
    }

    if (player.color == "red") {
        output_html += `
            <circle cx="40" cy="55" r="20" stroke-width="3" fill="red" />
            <line x1="40" y1="75" x2="40" y2="130" style="stroke:rgb(255,0,0);stroke-width:5" />
            <line x1="40" y1="90" x2="10" y2="70" style="stroke:rgb(255,0,0);stroke-width:5" />
            <line x1="40" y1="90" x2="70" y2="70" style="stroke:rgb(255,0,0);stroke-width:5" />
            <line x1="40" y1="130" x2="10" y2="160" style="stroke:rgb(255,0,0);stroke-width:5" />
            <line x1="40" y1="130" x2="70" y2="160" style="stroke:rgb(255,0,0);stroke-width:5" />
        `;
    } else {
        output_html += `
            <circle cx="40" cy="55" r="20" stroke-width="3" fill="blue" />
            <line x1="40" y1="75" x2="40" y2="130" style="stroke:rgb(0,0,255);stroke-width:5" />
            <line x1="40" y1="90" x2="10" y2="70" style="stroke:rgb(0,0,255);stroke-width:5" />
            <line x1="40" y1="90" x2="70" y2="70" style="stroke:rgb(0,0,255);stroke-width:5" />
            <line x1="40" y1="130" x2="10" y2="160" style="stroke:rgb(0,0,255);stroke-width:5" />
            <line x1="40" y1="130" x2="70" y2="160" style="stroke:rgb(0,0,255);stroke-width:5" />
        `;
    }

    output_html += '<text x="50%" y="61" text-anchor="middle" fill="white" font-size="20" font-weight="bold">'+player.id+'</text>';

    if (mode == 2) {
        output_html += '<text x="50%" y="185" text-anchor="middle" fill="black" font-size="15" font-weight="bold">'+player.moving_pts+'</text>';
    } else if (mode == 3) {
        output_html += `
            <text x="50%" y="185" text-anchor="middle" fill="black" font-size="15" font-weight="bold">`+player.moving_pts+`</text>
            <text x="50%" y="210" text-anchor="middle" fill="black" font-size="15" font-weight="bold">`+player.deduction_pts+`</text>
        `;
    }

    output_html += '</svg>';

    return output_html;
}