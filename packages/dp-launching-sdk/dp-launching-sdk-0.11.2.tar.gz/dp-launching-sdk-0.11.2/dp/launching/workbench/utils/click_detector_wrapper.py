from st_click_detector import click_detector


def click_detector_wrapper(rank: str, svg: str, label: str):
    content = f"""
        <a href='#' id='rank-{label}-{rank}'><span style="color: rgba(0, 0, 0, 0.45); margin-right: 10px">{svg}</span>{label}</a>
    """
    return click_detector(html_content=content, key=f"{rank}-{label}-detector")
