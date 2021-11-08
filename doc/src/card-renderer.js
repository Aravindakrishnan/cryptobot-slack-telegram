const commands = [
    {
        id : 1,
        name : "/getprice",
        option : "[coin_name] or [coin_symbol]",
        desc : "returns the current price of the coin default : USD"
    },
    {
        id : 2,
        name : "/getprice",
        option : "[coin_name] or [coin_symbol] [fiat_name]",
        desc : "returns the current price of the coin in fiat"
    },
    {
        id : 3,
        name : "/getdetail",
        option : "[coin_name] or [coin_symbol]",
        desc : "returns the complete detail about the current cryptocurrency"
    },
    {
        id : 4,
        name : "/getdetail",
        option : "[coin_name] or [coin_symbol] [fiat_name]",
        desc : "returns the complete detail about the current cryptocurrency with specific fiat price"
    },
    {
        id : 5,
        name : "/showgraph",
        option : "[coin_name or coin_symbol]",
        desc : "the candle graph snapshot of the particular coin <br> default : 1d"
    },
    {
        id : 6,
        name : "/showgraph",
        option : "[coin_name or coin_symbol] [1d,7d,1m,3m,1y,ytd,all]",
        desc : " return the candle graph snapshot of the particular coin's specific timeframe"
    }


]

const template = commands.map(command=> {

    return (
        `
        <div id=usage_card${command.id} class="usage__content">
        <span class="usage__command">${command.name}</span>
        <span class="usage__options">${command.option}</span>
        <p class="usage__desc">${command.desc}</p>
        </div>
        `
    )

})

document.querySelector(".usage-container").innerHTML = template.join("");