from ray import tune


class TunedFunction(object):
    def __init__(self, function, obj_function, param_space, **kwargs):
        """Create a wrapper around a function call that takes some hyperparameters as arguments.
        The tuner is a ray tuner.

        Args:
            function (Function): Main function to be called. 
            obj_function (Function): Objective function to evaluate the output from main function. 
                The objective function should have the same signature as the main function, plus an additional "output" args accepting the evaluated output of the main function. 
            param_space (dict[ray.tune]): Dictionary specifying the search space (use ray.tune). This is passed into a ray tuner. See ray.io for docs.

        Any additional arguments will be passed into the ray tuner. At minimum you can pass in tune_config=tune.TuneConfig(num_samples=10, metric='score', mode='min').

        Example::
            from maldives.env import *

            xx = np.linspace(0,1,101)
            def sinefunction(x,a=1):
                return np.sin(a*x)

            search_space = {'a':tune.uniform(0,10)}

            # we want to target a=3
            def loss(x,output=None, **kwargs):
                return {'loss':sum((output-np.sin(3*x))**2)}

            tune_config=tune.TuneConfig(num_samples=100, metric='loss', mode='min')
            tunedsine = TunedFunction(sinefunction, loss, search_space, run_config=air.RunConfig(verbose=0), tune_config=tune_config)

            plt.plot(tunedsine(xx))
            plt.plot(sinefunction(xx,3))
            plt.plot(tunedsine(xx, a=10)) # we can still explicitly override tuned parameter
        """
        self._function = function
        self._objective = obj_function
        self._params = param_space
        self._tuner_args = kwargs
        self.best_config = None
        self.tuner = None

    def __call__(self, *args, **kwargs):
        """Call the main function. We use tuned values for arguments that are in the search space and not specified.

        Returns:
            _type_: _description_
        """
        if self.best_config is None:
            self.optimize(*args, **kwargs)

        # fill in values from best config which are not explicitly specified.
        for k, v in self.best_config.items():
            if k not in kwargs:
                kwargs[k] = v

        return self._function(*args, **kwargs)

    def optimize(self, *args, **kwargs):
        """Optimize config based on passed inputs.
            This has the same signature as the main function. Arguments that are in the search space and not specified are tuned.
        """
        # if a config is explicitly specified, we do not want to optimize it.
        search_space = {k: v for k, v in self._params.items()
                        if k not in kwargs}

        def objective(config):
            output = self._function(*args, **kwargs, **config)
            return self._objective(*args, output=output, **kwargs, **config)

        self.tuner = tune.Tuner(
            objective, param_space=search_space, **self._tuner_args)
        results = self.tuner.fit()
        self.best_config = results.get_best_result().config
