const card_content = [
    {
        command_id : 1,
        command_name : "/getprice",
        command_option : "[coin_name] or [coin_symbol]",
        command_desc : "returns the current price of the coin default : USD"
    },
    {
        command_id : 2,
        command_name : "/getprice",
        command_option : "[coin_name] or [coin_symbol] [fiat_name]",
        command_desc : "returns the current price of the coin in fiat"
    },
    {
        command_id : 3,
        command_name : "/getdetail",
        command_option : "[coin_name] or [coin_symbol]",
        command_desc : "returns the complete detail about the current cryptocurrency"
    },
    {
        command_id : 4,
        command_name : "/getdetail",
        command_option : "[coin_name] or [coin_symbol] [fiat_name]",
        command_desc : "returns the complete detail about the current cryptocurrency with specific fiat price"
    },
    {
        command_id : 5,
        command_name : "/showgraph",
        command_option : "[coin_name or coin_symbol]",
        command_desc : "the candle graph snapshot of the particular coin <br> default : 1d"
    },
    {
        command_id : 5,
        command_name : "/showgraph",
        command_option : "[coin_name or coin_symbol] [1d,7d,1m,3m,1y,ytd,all]",
        command_desc : " return the candle graph snapshot of the particular coin's specific timeframe"
    }


]

const template = card_content.map(card=> {

    return (
        `
        <div id=usage_card${card.command_id} class="usage__content">
        <span class="usage__command">${card.command_name}</span>
        <span class="usage__options">${card.command_option}</span>
        <p class="usage__desc">${card.command_desc}</p>
        </div>
        `
    )

})

document.querySelector(".usage-container").innerHTML = template.join("");