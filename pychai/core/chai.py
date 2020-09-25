'''
Chai 基类
'''

import abc
from typing import Dict, List
from ..base import Character, Component, Compound, Degenerator, Selector
from ..util import loadInternal, loadGB, loadComponents, loadCompounds, loadConfig
from ..util import buildDegenerator, buildSelector, buildClassifier, buildRootMap, buildDegeneracy
import time

class Chai:
    def __init__(self, configPath):
        self.GB = loadGB()
        self.COMPONENTS = loadComponents()
        self.COMPOUNDS = loadCompounds(self.COMPONENTS)
        self.TOPOLOGY = loadInternal('../cache/topology.yaml')
        self.CONFIG = loadConfig(configPath)
        self.degenerator: Degenerator = buildDegenerator(self.CONFIG)
        self.selector: Selector = buildSelector(self.CONFIG)
        self.classifier = buildClassifier(self.CONFIG)
        self.rootMap = buildRootMap(self.CONFIG)
        self.compoundRootList, self.degeneracy = buildDegeneracy(self.CONFIG, self.degenerator, 
            self.COMPONENTS, self.COMPOUNDS)

    @abc.abstractmethod
    def _getComponentScheme(self, component: Component) -> None:
        pass

    @abc.abstractmethod
    def _getCompoundScheme(self, compound: Compound) -> None:
        pass

    @abc.abstractmethod
    def _encode(self, character: Character) -> None:
        pass

    def getComponentScheme(self) -> None:
        for component in self.COMPONENTS.values():
            self._getComponentScheme(component)

    def getCompoundScheme(self) -> None:
        for compound in self.COMPOUNDS.values():
            self._getCompoundScheme(compound)

    def encode(self) -> None:
        for characterName in self.GB:
            if characterName in self.COMPONENTS:
                character = self.COMPONENTS[characterName]
            else:
                character = self.COMPOUNDS[characterName]
            self._encode(character)

    def chai(self, fileName) -> None:
        t0 = time.time()
        self.getComponentScheme()
        t1 = time.time()
        self.getCompoundScheme()
        t2 = time.time()
        self.encode()
        t3 = time.time()
        print(t1 - t0, t2 - t1, t3 - t2)
        with open(fileName, 'w') as f:
            for characterName in self.GB:
                if characterName in self.COMPONENTS:
                    character = self.COMPONENTS[characterName]
                else:
                    character = self.COMPOUNDS[characterName]
                f.write('%s\t%s\n' % (characterName, character.code))
