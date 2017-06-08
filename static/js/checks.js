$(function () {

    var SECONDS = {name: "sec", nsecs: 1};
    var MINUTE = {name: "min", nsecs: 60};
    var HOUR = {name: "hr", nsecs: MINUTE.nsecs * 60};
    var DAY = {name: "day", nsecs: HOUR.nsecs * 24};
    var WEEK = {name: "week", nsecs: DAY.nsecs * 7};
    var MONTH = {name: "month", nsecs: DAY.nsecs * 30};
    var YEAR = {name: "year", nsecs: MONTH.nsecs * 12};
    var UNITS = [YEAR, MONTH, WEEK, DAY, HOUR, MINUTE, SECONDS];
    //add the various units e.g month, year ...centuary

    var secsToText = function(total) {
        var remainingSeconds = Math.floor(total);
        var result = "";
        for (var i=0, unit; unit=UNITS[i]; i++) {
            if (unit === WEEK && remainingSeconds % unit.nsecs != 0) {
                // Say "8 days" instead of "1 week 1 day"
                continue;
            }

            var count = Math.floor(remainingSeconds / unit.nsecs);
            remainingSeconds = remainingSeconds % unit.nsecs;

            if (count == 1) {
                result += "1 " + unit.name + " ";
            }

            if (count > 1) {
                result += count + " " + unit.name + "s ";
            }
        }

        return result;
    }

    function create_slider(tag_name) {
        let max_step = 60
        let min_step = 1
        noUiSlider.create(tag_name, {
            start: [20],
            connect: "lower",
            range: {
                'min': [MINUTE.nsecs, min_step],
                '10%': [HOUR.nsecs, min_step],
                '25%': [DAY.nsecs, max_step],
                '45%': [WEEK.nsecs, max_step],
                '60%': [MONTH.nsecs, max_step * max_step],
                'max': YEAR.nsecs

                //update the appropriate steps and intervals
                // ypdate the max va
            },
            pips: {
                mode: 'values',
                values: [MINUTE.nsecs, HOUR.nsecs, DAY.nsecs, WEEK.nsecs, MONTH.nsecs, YEAR.nsecs / 2,YEAR.nsecs],
                // values that apper on slider should be updated to reflect new intervals
                density: 4,
                format: {
                    to: secsToText,
                    from: function() {}
                }
            }
        });
    }


    var periodSlider = document.getElementById("period-slider");
    create_slider(periodSlider)
    periodSlider.noUiSlider.on("update", function(a, b, value) {
        var rounded = Math.round(value);
        $("#period-slider-value").text(secsToText(rounded));
        $("#update-timeout-timeout").val(rounded);
    });


    var graceSlider = document.getElementById("grace-slider");
    create_slider(graceSlider)
    graceSlider.noUiSlider.on("update", function(a, b, value) {
        var rounded = Math.round(value);
        $("#grace-slider-value").text(secsToText(rounded));
        $("#update-timeout-grace").val(rounded);
    });


    $('[data-toggle="tooltip"]').tooltip();

    $(".my-checks-name").click(function() {
        var $this = $(this);

        $("#update-name-form").attr("action", $this.data("url"));
        $("#update-name-input").val($this.data("name"));
        $("#update-tags-input").val($this.data("tags"));
        $('#update-name-modal').modal("show");
        $("#update-name-input").focus();

        return false;
    });

    $(".timeout-grace").click(function() {
        var $this = $(this);

        $("#update-timeout-form").attr("action", $this.data("url"));
        periodSlider.noUiSlider.set($this.data("timeout"))
        graceSlider.noUiSlider.set($this.data("grace"))
        $('#update-timeout-modal').modal({"show":true, "backdrop":"static"});

        return false;
    });

    $(".check-menu-remove").click(function() {
        var $this = $(this);

        $("#remove-check-form").attr("action", $this.data("url"));
        $(".remove-check-name").text($this.data("name"));
        $('#remove-check-modal').modal("show");

        return false;
    });


    $("#my-checks-tags button").click(function() {
        // .active has not been updated yet by bootstrap code,
        // so cannot use it
        $(this).toggleClass('checked');

        // Make a list of currently checked tags:
        var checked = [];
        $("#my-checks-tags button.checked").each(function(index, el) {
            checked.push(el.textContent);
        });

        // No checked tags: show all
        if (checked.length == 0) {
            $("#checks-table tr.checks-row").show();
            $("#checks-list > li").show();
            return;
        }

        function applyFilters(index, element) {
            var tags = $(".my-checks-name", element).data("tags").split(" ");
            for (var i=0, tag; tag=checked[i]; i++) {
                if (tags.indexOf(tag) == -1) {
                    $(element).hide();
                    return;
                }
            }

            $(element).show();
        }

        // Desktop: for each row, see if it needs to be shown or hidden
        $("#checks-table tr.checks-row").each(applyFilters);
        // Mobile: for each list item, see if it needs to be shown or hidden
        $("#checks-list > li").each(applyFilters);

    });

    $(".pause-check").click(function(e) {
        var url = e.target.getAttribute("data-url");
        $("#pause-form").attr("action", url).submit();
        return false;
    });


    $(".usage-examples").click(function(e) {
        var a = e.target;
        var url = a.getAttribute("data-url");
        var email = a.getAttribute("data-email");

        $(".ex", "#show-usage-modal").text(url);
        $(".em", "#show-usage-modal").text(email);

        $("#show-usage-modal").modal("show");
        return false;
    });


    var clipboard = new Clipboard('button.copy-link');
    $("button.copy-link").mouseout(function(e) {
        setTimeout(function() {
            e.target.textContent = "copy";
        }, 300);
    })

    clipboard.on('success', function(e) {
        e.trigger.textContent = "copied!";
        e.clearSelection();
    });

    clipboard.on('error', function(e) {
        var text = e.trigger.getAttribute("data-clipboard-text");
        prompt("Press Ctrl+C to select:", text)
    });

    //callback to select priority
    $("select#priority").change( function() {
        let priority_value = $(this).val();
        let check_url = $(this).data('url')
        let token = $('input[name="csrfmiddlewaretoken"]').val();
        
        //Execute the post request to update the priority of this check
        $.post( check_url, { priority: priority_value, csrfmiddlewaretoken: token }).done(function( data ) {
                //Upon success posting, refresh the page to effect the sorting of jobs
                location.reload(true);
        });

    })

});
