import {useForm} from "react-hook-form"
import CustomButton from "../../Boton/CustomButton";
import "./FormCrearPartida.css"

function FormCrearPartida()
{
    const USERNAME = "Juæn";

    const {
        register,
        handleSubmit,
        formState: { errors },
        watch,
        setValue,
        reset,
      } = useForm({
        defaultValues: {
          nombrePartida: "Partida de " + USERNAME,
          minPlayers: 4,
          maxPlayers: 12,
          contraseña: ""
        },
      });

    const FORM_SUBMIT = handleSubmit((data) => {
        console.log(data);
        reset();
    });

    return(
    <> 
        <h2>Formulario de Creación</h2>
        <body>
            <form onSubmit={FORM_SUBMIT}>
                <div>
                    <label>Nombre de la Partida</label>
                    <input
                        type="text"
                        name="nombrePartida"
                        {...register("nombrePartida", {
                            required: {
                                value: true,
                                message: "Nombre de la partida requerido"
                            },
                            maxLength: {
                                value: 20,
                                message: "Nombre de la partida demasiado largo"
                            },
                            minLength: {
                                value: 4,
                                message: "Nombre de la partida demasiado corto"
                            }
                        })} />
                    {errors.nombrePartida && <p>{errors.nombrePartida.message}</p>}
                </div>

                <div>
                    <label>Mínimo de Jugadores</label>
                    <input
                        type="number"
                        name="minPlayers"
                        {...register("minPlayers", {
                            required: {
                                value: "",
                                message: "Mínimo de jugadores requerido"
                            },
                            max: {
                                value: 12,
                                message: "Mínimo de jugadores demasiado alto"
                            },
                            min: {
                                value: 4,
                                message: "Mínimo de jugadores demasiado bajo"
                            }
                        })} />
                </div>

                <div>
                    <label>Máximo de Jugadores</label>
                    <input
                        type="number"
                        name="maxPlayers"
                        {...register("maxPlayers", {
                            required: {
                                value: "",
                                message: "Máximo de jugadores requerido"
                            },
                            max: {
                                value: 12,
                                message: "Máximo de jugadores demasiado alto"
                            },
                            min: {
                                value: 4,
                                message: "Máximo de jugadores demasiado bajo"
                            }
                        })} />
                </div>

                <div>
                    <label>Contraseña</label>
                    <input
                        type="password"
                        name="contraseña"
                        {...register("contraseña", {
                            maxLength: {
                                value: 20,
                                message: "Contraseña demasiado larga"
                            },
                            minLength: {
                                value: 4,
                                message: "Contraseña demasiado corta"
                            }
                        })} />
                </div>

                <CustomButton label="Crear Partida" onClick={FORM_SUBMIT} />
            </form>
        </body></>
    );
}

export default FormCrearPartida