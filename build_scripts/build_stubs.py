"""
Generates needed files from templates in order to complete the package.
"""
from __future__ import annotations

import itertools
import logging
import sys
from typing import cast

import marko
import requests
from jinja2 import Environment, PackageLoader

EVENT_TYPES_RAW_URL = "https://raw.githubusercontent.com/mdn/content/main/files/en-us/web/events/index.md"
EVENT_TYPES_OUTPUT_PATH = "src/pyscript/types/event_types.pyi"
j_env = Environment(loader=PackageLoader("build_stubs"))
j_event_types = j_env.get_template("event_types.pyi")


def execute() -> None:
    """
    Execute the procedure to generate dynamic stub files.
    """
    logging.info("Generating dynamic files for pyscript-stubs...")

    logging.info("Preparing event_types.pyi from template")
    event_types_rendered = prepare_event_types_pyi()
    logging.info(f"Writing {EVENT_TYPES_OUTPUT_PATH}")
    with open(EVENT_TYPES_OUTPUT_PATH, "w") as f:
        f.write(event_types_rendered)


def _identify_list_of_list_filter(element: marko.block.Element) -> bool:
    """
    Filter a BlockElements in order to determine if it is a list of lists.

    :param element: The element to validate.
    :return: If this element is a list of a lists.
    :raise: TypeError when the first child of a list is not a ListItem
    """
    if not isinstance(element, marko.block.List):
        return False
    # We only need to validate the first ListItem
    if not isinstance(element.children[0], marko.block.ListItem):
        raise TypeError(
            f"When parsing {element} found that first child {element.children[0]} was not a ListItem. Aborting"
        )
    sub_lists = list(
        filter(lambda e: isinstance(e, marko.block.List), cast(marko.block.ListItem, element.children[0]).children)
    )
    # Check if we got any hits
    return len(sub_lists) > 0


def _identify_sublist_elements_paragraph_link_text(elements: list[marko.block.Element]) -> bool:
    """
    Filter elements in order to determine if they match the expected structure of a list item link.

    The elements should contain a single element of a Paragraph, which itself will contain a single element of a Link,
    which itself will contain a single element of a RawText

    :param elements: children of the list item we want to validate
    :return: if this element is what we're looking for
    """
    if len(elements) != 1:
        logging.debug(f"Parse Paragraph: Passed {len(elements)} elements expected 1 element.")
        return False
    element = elements[0]
    if not isinstance(element, marko.block.Paragraph):
        logging.debug(f"Parse Paragraph: Element <{element}> was not of type Paragraph.")
        return False
    if len(element.children) != 1:
        logging.debug(f"Parse Paragraph: Element had {len(element.children)} children, expected 1 child.")
        return False
    child_element = element.children[0]
    if not isinstance(child_element, marko.block.inline.Link):
        logging.debug(f"Parse Paragraph: Element child <{child_element}> was not of type Link.")
        return False
    if len(child_element.children) != 1:
        logging.debug(
            f"Parse Paragraph: Element grandchild had {len(child_element.children)} children, expected 1 child."
        )
        return False
    grandchild_element = child_element.children[0]
    if not isinstance(grandchild_element, marko.block.inline.RawText):
        logging.debug(f"Parse Paragraph: Element grandchild <{grandchild_element}> was not of type RawText.")
        return False
    return True


def _map_get_raw_text_from_paragraph(elements: list[marko.block.Element]) -> str:
    """
    Take the Paragraphs with the link and extract the raw text.

    :param elements: The list of elements to parse.
    :return: The raw string
    :raise: TypeError if it not a valid paragraph
    """
    if not _identify_sublist_elements_paragraph_link_text(elements):
        raise TypeError("The provided elements were not a Paragraph element with required Link and RawText children.")
    return marko.render(
        cast(
            marko.block.inline.Link, cast(marko.block.Paragraph, elements[0]).children[0]  # type: ignore[arg-type]
        ).children[0]
    )


def _map_list_of_list_into_sublist_elements(element: marko.block.ListItem) -> list[list[marko.block.Element]]:
    """
    Find the List within a ListItem and return the ListItem Elements.

    :param element: The ListItem Element to process.
    :return: The elements of each ListItem in the list.
    """
    list_items = []
    for list_element in filter(lambda e: isinstance(e, marko.block.List), element.children):
        for listitem_element in cast(marko.block.List, list_element).children:
            list_items.append(list(cast(marko.block.ListItem, listitem_element).children))
    return list_items


def prepare_event_types_pyi() -> str:
    """
    Prepare the `event_types.pyi` file and output the file contents.
    """
    logging.debug(f"Fetching {EVENT_TYPES_RAW_URL}")
    r = requests.get(EVENT_TYPES_RAW_URL)
    logging.debug(f"Parsing {EVENT_TYPES_RAW_URL}")
    md = marko.parse(r.text)

    # The events are encoded as a list of lists, and are they only list of lists in the document
    md_found_list_of_lists = cast(list[marko.block.List], list(filter(_identify_list_of_list_filter, md.children)))
    if len(md_found_list_of_lists) != 1:
        raise RuntimeError(
            f"This generator assumes there is 1 list of lists in the document but we found "
            f"{len(md_found_list_of_lists)}."
        )
    md_list_of_lists = md_found_list_of_lists[0]

    # The primary list is the different classes of events, and the secondary lists are links the events themselves.
    md_lists = list(
        itertools.chain.from_iterable(
            map(_map_list_of_list_into_sublist_elements, cast(list[marko.block.ListItem], md_list_of_lists.children))
        )
    )
    # Each element should contain a single Paragraph that contains a LinkObject that contains RawText.
    # We want to extract the RawText from each element.
    md_list_raw = list(map(_map_get_raw_text_from_paragraph, md_lists))

    # Each raw string should <event>_event (_ = space), so we can strip "_event" from the end.
    event_types = list(map(lambda s: s.removesuffix(" event"), md_list_raw))
    logging.info("Rendering event_types.pyi")
    return j_event_types.render(events=event_types)


if __name__ == "__main__":
    # When calling the script directly, setup logging before calling execute()
    logging.basicConfig(stream=sys.stderr, encoding="utf-8", level=logging.DEBUG)
    execute()
