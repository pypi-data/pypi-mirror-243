import datetime

import numpy as np
import pandas as pd
import pytest
import pytz

from arthurai import ArthurAttribute, ArthurModel
from arthurai.common.constants import ValueType, Stage, OutputType, InputType, InferenceType

from tests.fixtures.mocks import client

GROUND_TRUTH = "gt"
TEMPO = "tempo"
PRED = "recommendations"
TIME_SERIES = "bill_pay_history"
TIME = "time"

RANKED_LIST_DATAFRAME = pd.DataFrame({
    TIME_SERIES: [[{"timestamp": datetime.datetime(2011, 8, 15, 0, 0, 0, 0, pytz.UTC), "value": 1},
                   {"timestamp": datetime.datetime(2011, 8, 16, 0, 0, 0, 0, pytz.UTC), "value": 2},
                   {"timestamp": datetime.datetime(2011, 8, 17, 0, 0, 0, 0, pytz.UTC), "value": 3}],
                  [{"timestamp": datetime.datetime(2011, 8, 25, 0, 0, 0, 0, pytz.UTC), "value": 3},
                   {"timestamp": datetime.datetime(2011, 8, 26, 0, 0, 0, 0, pytz.UTC), "value": 2},
                   {"timestamp": datetime.datetime(2011, 8, 27, 0, 0, 0, 0, pytz.UTC), "value": 1}]],
    TIME: ["2011-08-25T00:00:00Z", "2011-08-28T00:00:00Z",],
    TEMPO: [88, 66],
    PRED: [
        [{"item_id": "1", "label": "test", "score": 0.88},
         {"item_id": "2", "label": "test", "score": 0.88}],
        [{"item_id": "1", "label": "test", "score": 0.66},
         {"item_id": "2", "label": "test", "score": 0.66}],
    ],
    GROUND_TRUTH: [["test1", "test2"], ["test3", "test4"]]
})

RANKED_LIST_JSON = [
    {
        InferenceType.REFERENCE_DATA: {
            TIME_SERIES: [
                {"timestamp": "2011-08-15T00:00:00+00:00", "value": 1},
                {"timestamp": "2011-08-16T00:00:00+00:00", "value": 2},
                {"timestamp": "2011-08-17T00:00:00+00:00", "value": 3}
            ],
            TIME: "2011-08-25T00:00:00Z",
            TEMPO: 88,
            PRED: [
                {"item_id": "1", "label": "test", "score": 0.88},
                {"item_id": "2", "label": "test", "score": 0.88}
            ],
            GROUND_TRUTH: ["test1", "test2"],
        }
    },
    {
        InferenceType.REFERENCE_DATA: {
            TIME_SERIES: [
                {"timestamp": "2011-08-25T00:00:00+00:00", "value": 3},
                {"timestamp": "2011-08-26T00:00:00+00:00", "value": 2},
                {"timestamp": "2011-08-27T00:00:00+00:00", "value": 1}
            ],
            TIME: "2011-08-28T00:00:00Z",
            TEMPO: 66,
            PRED: [
                {"item_id": "1", "label": "test", "score": 0.66},
                {"item_id": "2", "label": "test", "score": 0.66}
            ],
            GROUND_TRUTH: ["test3", "test4"]
        }
    }
]

TEMPO_ATTR = ArthurAttribute(name=TEMPO,
                             value_type=ValueType.Integer,
                             stage=Stage.NonInputData,
                             position=0)

TIME_ATTR = ArthurAttribute(name=TIME,
                            value_type=ValueType.Timestamp,
                            stage=Stage.NonInputData,
                            position=1)

TIME_SERIES_ATTR = ArthurAttribute(name=TIME_SERIES,
                                   value_type=ValueType.TimeSeries,
                                   stage=Stage.ModelPipelineInput,
                                   position=0)

GT_ATTR = ArthurAttribute(
            name=GROUND_TRUTH,
            stage=Stage.GroundTruth,
            value_type=ValueType.StringArray,
            attribute_link=PRED,
            position=0)

PRED_ATTR = ArthurAttribute(
            name=PRED,
            stage=Stage.PredictedValue,
            value_type=ValueType.RankedList,
            attribute_link=GROUND_TRUTH,
            position=0)

RANKED_LIST_MODEL_ATTRIBUTES = [TEMPO_ATTR, TIME_ATTR, GT_ATTR, PRED_ATTR, TIME_SERIES_ATTR]

MODEL_DATA = {"partner_model_id": "test",
              "input_type": InputType.TimeSeries,
              "output_type": OutputType.RankedList}

MODEL_ID = "c4ea58b6-4ec7-43b2-94d3-786eccb2a492"


@pytest.fixture
def ranked_list_model(client):
    model = ArthurModel(
        **MODEL_DATA,
        client=client.client,
        attributes=RANKED_LIST_MODEL_ATTRIBUTES
    )
    model.id = MODEL_ID
    return model
