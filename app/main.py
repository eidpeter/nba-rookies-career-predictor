from pydantic import BaseModel
from fastapi import FastAPI
from typing import List, Optional
from fastapi.responses import RedirectResponse
import numpy as np
import pickle as pkl

app = FastAPI()

# load the model
with open("models/nba_classifier.pkl", "rb") as file:
    model = pkl.load(file)


class Player(BaseModel):
    """The Player model, that will be the input to the predict endpoint.
    """
    name: Optional[str] = None
    games_played: int
    minutes_per_game: float
    points_per_game: float
    field_goals_made_per_game: float


class Prediction(BaseModel):
    """The Prediction model, that will be the output of the predict endpoint.
    """
    prediction: str
    message: str


@app.get("/", include_in_schema=False)
def redirect_root():
    """Redirects to the docs.
    """
    return RedirectResponse(url='/docs')


@app.post("/predict", response_model=Prediction)
def predict(player: Player):
    """The predict endpoint, that will take a Player and return a Prediction.
    """
    data = np.array(
        [
            [
                player.games_played,
                player.minutes_per_game,
                player.points_per_game,
                player.field_goals_made_per_game,
            ]
        ]
    )

    prediction = model.predict(data)[0]
    msg = f"{player.name} is likely to be an NBA player in 5 years." if prediction == 1 else f"{player.name} is not likely be an NBA player after 5 years."

    return Prediction(prediction=prediction.astype(str), message=msg)
