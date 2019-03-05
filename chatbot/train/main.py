# Copyright 2019 Contributors to Hyperledger Sawtooth
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -----------------------------------------------------------------------------

import argparse
import os
import sys
from os.path import dirname as DIRNAME

from rasa_nlu.training_data import load_data
from rasa_nlu.model import Trainer
from rasa_nlu import config

from rasa_core.agent import Agent
from rasa_core.policies.memoization import MemoizationPolicy
from rasa_core.policies.keras_policy import KerasPolicy
from rasa_core.policies.fallback import FallbackPolicy
from rbac.common.logs import get_default_logger

LOGGER = get_default_logger(__name__)

TOP_DIR = DIRNAME(DIRNAME(__file__))
CONFIG_DIR = os.path.join(TOP_DIR, "config")

NLU_DATA = os.path.join(TOP_DIR, "data/nlu.md")
CORE_DATA = os.path.join(TOP_DIR, "data/stories.md")
NLU_MODEL = os.path.join(TOP_DIR, "models/")
CORE_MODEL = os.path.join(TOP_DIR, "models/current/core")

NLU_CONFIG = os.path.join(CONFIG_DIR, "nlu_config.yml")
CORE_DOMAIN = os.path.join(CONFIG_DIR, "domain.yml")


def parse_args(args):
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--nlu", help="Train the language processing model", action="store_true"
    )
    parser.add_argument(
        "--core", help="Train the dialog engine model", action="store_true"
    )
    return parser.parse_args(args)


def train_nlu():
    LOGGER.info("[NLU] Loading training data from %s", NLU_DATA)
    training_data = load_data(NLU_DATA)

    LOGGER.info("[NLU] Loading config from %s", NLU_CONFIG)
    trainer = Trainer(config.load(NLU_CONFIG))

    LOGGER.info("[NLU] Training NLU...")
    trainer.train(training_data)
    trainer.persist(NLU_MODEL, fixed_model_name="nlu", project_name="current")


def train_core():
    keras = KerasPolicy(max_history=5)
    memoization = MemoizationPolicy(max_history=5)
    fallback = FallbackPolicy(nlu_threshold=0.28)

    LOGGER.info("[CORE] Creating agent from YAML at %s", CORE_DOMAIN)
    agent = Agent(CORE_DOMAIN, policies=[memoization, keras, fallback])

    LOGGER.info("[CORE] Loading training data from %s", CORE_DATA)
    data = agent.load_data(CORE_DATA)

    LOGGER.info("[CORE] Training Core...")
    agent.train(data)
    agent.persist(CORE_MODEL)


def main():
    opts = parse_args(sys.argv[1:])
    if opts.nlu:
        train_nlu()
    if opts.core:
        train_core()
