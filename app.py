
import panel as pn
import os
import openai

pn.extension()

# Configurar la clave de API desde variable de entorno
openai.api_key = os.getenv("GROQ_API_KEY")
GROQ_MODEL = "llama3-8b-8192"

# Prompt del sistema
system_prompt = """
Sos HeladoBot, un asistente virtual especializado en tomar pedidos de helado para una heladería artesanal.

Tu objetivo es asistir al cliente paso a paso para completar un pedido claro y detallado.

🧭 Flujo que debés seguir:
1. Saludá al cliente con simpatía.
2. Preguntá qué sabor o sabores desea (podés sugerir si lo pide).
3. Consultá qué tamaño quiere: chico (1 bocha), mediano (2 bochas), grande (3 bochas).
4. Preguntá si quiere toppings extra: salsa de chocolate, granas, dulce de leche, frutas, crocante (cada uno cuesta $200).
5. Preguntá si quiere agregar bebida (agua $500, soda $600).
6. Preguntá si el pedido es para llevar o consumir en el local.
7. Al final, mostrá un resumen con:
   - Tamaño
   - Sabores
   - Toppings
   - Bebida
   - Precio total

🎨 Estilo de respuesta:
- Sé breve, simpático y conversacional.
- Hablá en castellano neutro.
- Nunca respondas todo junto: solo hacé 1 paso por vez.
- Siempre pedí confirmación antes de cerrar.

🚫 No inventes sabores ni precios.
🚫 No asumas nada sin que el cliente lo haya dicho.

Menú de sabores:
- chocolate
- dulce de leche
- frutilla
- vainilla
- oreo
- limón
- maracuyá
- crema del cielo

Tamaños:
- chico ($1000)
- mediano ($1500)
- grande ($2000)

Toppings ($200 cada uno): salsa de chocolate, granas, dulce de leche, frutas, crocante

Bebidas: agua ($500), soda ($600)

Sos un bot simpático pero preciso. Tu prioridad es que el pedido sea completo y claro.
"""

# Función para conectarse a Groq
def get_completion_from_messages(messages, model=GROQ_MODEL, temperature=0.7):
    client = openai.OpenAI(
        api_key=os.environ["GROQ_API_KEY"],
        base_url="https://api.groq.com/openai/v1"
    )
    response = client.chat.completions.create(
        model=model,
        messages=messages,
        temperature=temperature
    )
    return response.choices[0].message.content

# Conversación inicial
context = [
    {"role": "system", "content": system_prompt}
]

output = pn.Column()

def collect_messages(_):
    user_input = inp.value
    inp.value = ""
    context.append({"role": "user", "content": user_input})
    response = get_completion_from_messages(context)
    context.append({"role": "assistant", "content": response})

    # Mostrar mensajes como burbujas
    output.append(pn.Row("🧑: ", pn.pane.HTML(f"<div style='background-color:#ffffff; padding:10px; border-radius:5px'>{user_input}</div>", width=500)))
    output.append(pn.Row("🤖: ", pn.pane.HTML(f"<div style='background-color:#f2f2f2; padding:10px; border-radius:5px'>{response}</div>", width=500)))

inp = pn.widgets.TextInput(placeholder="Escribí tu pedido...")
button = pn.widgets.Button(name="Enviar")
button.on_click(collect_messages)

dashboard = pn.Column(
    pn.pane.Markdown("## 🍨 Bienvenido a HeladoBot"),
    inp,
    button,
    output
)

dashboard.servable()

