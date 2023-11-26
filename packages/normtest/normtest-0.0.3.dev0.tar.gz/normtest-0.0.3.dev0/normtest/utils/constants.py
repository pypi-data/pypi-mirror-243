# This file is used to store some CONSTANTS and minor other things

import warnings

REJECTION = "Reject H₀"
ACCEPTATION = "Fail to reject H₀"

HYPOTESES = """`H₀`: Data was sampled from a Normal distribution.
`H₁`: The data was sampled from a distribution other than the Normal distribution."""


def warning_plot():
    def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
        return "%s:%s: %s: %s\n" % (filename, lineno, category.__name__, message)

    warnings.formatwarning = warning_on_one_line

    warnings.warn(
        "This function is experimental and its behavior may not be ideal.", stacklevel=3
    )


def user_warning(text):
    def warning_on_one_line(message, category, filename, lineno, file=None, line=None):
        return "%s:%s: %s: %s\n" % (filename, lineno, category.__name__, message)

    warnings.formatwarning = warning_on_one_line

    warnings.warn(text, stacklevel=3)


seaborn_colors = {
    "deep": [
        (0.2980392156862745, 0.4470588235294118, 0.6901960784313725),
        (0.8666666666666667, 0.5176470588235295, 0.3215686274509804),
        (0.3333333333333333, 0.6588235294117647, 0.40784313725490196),
        (0.7686274509803922, 0.3058823529411765, 0.3215686274509804),
        (0.5058823529411764, 0.4470588235294118, 0.7019607843137254),
        (0.5764705882352941, 0.47058823529411764, 0.3764705882352941),
        (0.8549019607843137, 0.5450980392156862, 0.7647058823529411),
        (0.5490196078431373, 0.5490196078431373, 0.5490196078431373),
        (0.8, 0.7254901960784313, 0.4549019607843137),
        (0.39215686274509803, 0.7098039215686275, 0.803921568627451),
        (0.00392156862745098, 0.45098039215686275, 0.6980392156862745),
        (0.8705882352941177, 0.5607843137254902, 0.0196078431372549),
        (0.00784313725490196, 0.6196078431372549, 0.45098039215686275),
    ],
    "colorblind": [
        (0.00392156862745098, 0.45098039215686275, 0.6980392156862745),
        (0.8705882352941177, 0.5607843137254902, 0.0196078431372549),
        (0.00784313725490196, 0.6196078431372549, 0.45098039215686275),
        (0.8352941176470589, 0.3686274509803922, 0.0),
        (0.8, 0.47058823529411764, 0.7372549019607844),
        (0.792156862745098, 0.5686274509803921, 0.3803921568627451),
        (0.984313725490196, 0.6862745098039216, 0.8941176470588236),
        (0.5803921568627451, 0.5803921568627451, 0.5803921568627451),
        (0.9254901960784314, 0.8823529411764706, 0.2),
        (0.33725490196078434, 0.7058823529411765, 0.9137254901960784),
    ],
}
