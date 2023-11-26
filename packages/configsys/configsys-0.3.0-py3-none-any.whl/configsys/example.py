from dataclasses import dataclass

from configsys.config import ConfigMixin


# We recommend using kw_only=True to make sure Configs are specified explicitly
class ImageDataLoader:
    @dataclass(kw_only=True)
    class Config(ConfigMixin):
        _target_ = "configsys.example.ImageDataLoader"
        batch_size: int
        shuffle: bool

    def __init__(self, config: Config):
        self.config = config

    def get_data(self):
        return dict(x=[2, 3], y=[4, 5])


class TextDataLoader:
    @dataclass(kw_only=True)
    class Config(ConfigMixin):
        _target_ = "configsys.example.TextDataLoader"
        batch_size: int
        shuffle: bool

    def __init__(self, config: Config):
        self.config = config

    def get_data(self, x):
        return dict(x=['hello', 'world'])


class MLP:
    @dataclass(kw_only=True)
    class Config(ConfigMixin):
        _target_ = "configsys.example.MLP"
        n_layers: int
        n_hidden: int

    def __init__(self, config: Config):
        self.config = config

    def forward(self, x):
        return x


class Transformer:
    @dataclass(kw_only=True)
    class Config(ConfigMixin):
        _target_ = "configsys.example.Transformer"
        n_heads: int

    def __init__(self, config: Config):
        self.config = config

    def forward(self, x):
        return x


# You won't always specify a _target_, for example, when the config is for a class you did not write
@dataclass(kw_only=True)
class TrainerConfig(ConfigMixin):
    dataloader: ImageDataLoader.Config | TextDataLoader.Config
    model: MLP.Config | Transformer.Config
    learning_rate: float
    steps: int


class Trainer:
    def __init__(self, dataloader: ImageDataLoader | TextDataLoader,
                 model: MLP | Transformer,
                 learning_rate: float,
                 steps: int):
        self.dataloader = dataloader
        self.model = model
        self.learning_rate = learning_rate
        self.steps = steps

    def train(self):
        print("{self} training...")
        print(self.learning_rate)
        print(self.steps)


def main(outdir):
    for model_config in [MLP.Config(n_layers=3, n_hidden=128), Transformer.Config(n_heads=6)]:
        config = TrainerConfig(
            dataloader=ImageDataLoader.Config(batch_size=32, shuffle=True),
            model=model_config,
            learning_rate=0.1,
            steps=100,
        )
        model = config.model.instantiate_target()  # equivalent to Model(config=config.model)
        dataloader = config.dataloader.instantiate_target()  # equivalent to DataLoader(config=config.dataloader)
        trainer = Trainer(dataloader, model, config.learning_rate, config.steps)
        trainer.train()

        config.to_yaml_file(f"{outdir}/trainer_config.yaml")

        trainer_config2 = TrainerConfig.from_yaml_file(f"{outdir}/trainer_config.yaml")
        assert config == trainer_config2


if __name__ == '__main__':
    main('.')
