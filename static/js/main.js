$( document ).ready(() => {

    let field = $("#chart_func");
    let func_name = $("#func_name");
    let step_name = $("#step_name");
    let error = false;

    let paramB = 0.01;
    let paramX0 = 0;
    let paramY0 = 0;

    // chart configs
    let options = {
        ///Boolean - Whether grid lines are shown across the chart
        scaleShowGridLines: false,
        //String - Colour of the grid lines
        scaleGridLineColor: "rgba(0,0,0,.05)",
        //Number - Width of the grid lines
        scaleGridLineWidth: 1,
        //Boolean - Whether to show horizontal lines (except X axis)
        scaleShowHorizontalLines: true,
        //Boolean - Whether to show vertical lines (except Y axis)
        scaleShowVerticalLines: true,
        //Boolean - Whether the line is curved between points
        bezierCurve: true,
        //Number - Tension of the bezier curve between points
        bezierCurveTension: 0.4,
        //Boolean - Whether to show a dot for each point
        pointDot: false,
        //Number - Radius of each point dot in pixels
        pointDotRadius: 4,
        //Number - Pixel width of point dot stroke
        pointDotStrokeWidth: 1,
        //Number - amount extra to add to the radius to cater for hit detection outside the drawn point
        pointHitDetectionRadius: 0,
        //Boolean - Whether to show a stroke for datasets
        datasetStroke: true,
        //Number - Pixel width of dataset stroke
        datasetStrokeWidth: 2,
        //Boolean - Whether to fill the dataset with a colour
        datasetFill: true,
        showXLabels: 10,
    };
    let labels = [];
    for (let i = 0; i < 100; ++i) {
        labels.push(i);
    }
    let data = {
        labels: labels,
        datasets: [{
            label: "ρ(w)",
            fillColor: "rgba(173,224,214,0.2)",
            strokeColor: "rgba(0,136,255,0.4)",
            pointColor: "rgba(220,220,220,1)",
            pointStrokeColor: "#fff",
            pointHighlightFill: "#fff",
            pointHighlightStroke: "rgba(220,220,220,1)",
            data: []
        }]
    };

    // default value
    let cur_step = 0;
    let cur_func;
    let cur_func_validated;

    // show current state
    switchToStep(1);

    field.on('input', (event) => {
        let new_func;
        if (event.target.value.length == 0) {
            new_func = validate(get_func(cur_step));
        } else {
            new_func = validate(event.target.value);
        }
         if (new_func) {
             console.log(cur_func);
             cur_func = event.target.value;
             if (cur_func.length == 0) cur_func = get_func(cur_step);
             cur_func_validated = new_func;
             try {
                 update_chart();
                 error = false;
                 field.removeClass("form-error");
             } catch (exc) {
                 error = true;
                 field.addClass("form-error");
             }
         } else {
             error = true;
             field.addClass("form-error");
         }
    });

    $(".step").on('click', (event) => {
        event.preventDefault();
       switchToStep(parseInt(event.target.id.substring(4)));
    });

    $(".btn").on('click', (event) => {
        event.preventDefault();
        if (error) return;
        if (cur_step == 1 || cur_step == 2 || cur_step == 4) {
            update_func(cur_step, cur_func);
        }
        if (cur_step == 3) {
            update_params();
        }
        switchToStep(cur_step + 1)
    });

    function switchToStep(new_step) {
        // TODO: change it later
        if (new_step == 6) {
             $.post('/', {'action': "run_tests"});
            return;
        }
        if (new_step == cur_step) return;
        $("#step" + cur_step).removeClass("step-active");
        $("#step" + new_step).addClass("step-active");
        cur_step = new_step;

        step_name.text(generate_name(cur_step));
        field[0].value = "";
        document.getElementById("main_btn").innerHTML = 'Next';

        if (cur_step == 1 || cur_step == 2 || cur_step == 4) {
            clear3step_fields();
            let func_field = document.getElementById('first_form_div');
            if (func_field != null) func_field.style.display = 'block';
            func_name.text(get_func_name(cur_step));
            cur_func = get_func(cur_step);
            cur_func_validated = validate(cur_func);
            field[0].placeholder = cur_func;
            update_chart();
        } else if (cur_step == 3) {
            clear124step_fields();
            func_name.text('parameter β:');
            field[0].placeholder = '0.01';
            $('.second_title').append('<li class="func-f" id="sec-title">f(z, x, S, β) = β(x - z)</li>');
            $( '<div class="form-group" id="pb"><label for="param_b">parameter β</label><input type="number" class="form-control" id="param_b" placeholder="' + paramB + '"></div>').insertBefore( '#main_btn' );
            $( '<div class="form-group" id="px"><label for="param_x">parameter X0</label><input type="number" class="form-control" id="param_x" placeholder="' + paramX0 + '"></div>').insertBefore( '#main_btn' );
            $( '<div class="form-group" id="py"><label for="param_y">parameter Y0</label><input type="number" class="form-control" id="param_y" placeholder="' + paramY0 + '"></div>').insertBefore( '#main_btn' );
            add_listeners();
        } else {
        //    step with results
            clear124step_fields();
            clear3step_fields();
            document.getElementById("main_btn").innerHTML = 'Run Tests';
        }
    }

    function update_chart() {

        let values = [];
        let labels = [];
        for (let i = 0; i < 100; ++i) {
            let scope = get_scope(cur_step, i);
            if (cur_step == 1) {
                labels.push(i / 100)
            } else {
                labels.push(i)
            }
            values.push(apply_func(cur_func_validated, scope));
        }

        $('#myChart').remove();
        $('.chart-container').append('<canvas id="myChart"><canvas>');
        var ctx = document.getElementById("myChart").getContext("2d");
        ctx.canvas.width = 540;
        ctx.canvas.height = 300;

        data.datasets[0].data = values;
        data.labels = labels;

        new Chart(ctx).Line(data, options);
    }

    function clear3step_fields() {
        let sec_title = document.getElementById("sec-title");
        if (sec_title != null) sec_title.remove();
        let px =  document.getElementById("px");
        if (px != null) px.remove();
        let py =  document.getElementById("py");
        if (py != null) py.remove();
        let pb =  document.getElementById("pb");
        if (pb != null) pb.remove();
    }

    function clear124step_fields() {
        $('#myChart').remove();
        let func_field = document.getElementById('first_form_div');
        if (func_field != null) func_field.style.display = 'none';
    }

    function update_params() {
        $.post('/', {'action': "update_params", "paramB": paramB,
                     "paramX": paramX0, "paramY": paramY0});
    }

    function add_listeners() {
        let pBField = $("#param_b");
        let pXField = $("#param_x");
        let pYField = $("#param_y");
        let new_value;
        pBField.on('input', (event) => {
            new_value = parseInt(event.target.value);
            if (!isNaN(new_value)) {
                paramB = new_value;
                pBField.removeClass("form-error");
            } else {
                pBField.addClass("form-error");
            }
        });
        pXField.on('input', (event) => {
            new_value = parseInt(event.target.value);
            if (!isNaN(new_value)) {
                paramX0 = new_value;
                pXField.removeClass("form-error");
            } else {
                pXField.addClass("form-error");
            }
        });
        pYField.on('input', (event) => {
            new_value = parseInt(event.target.value);
            if (!isNaN(new_value)) {
                paramY0 = new_value;
                pYField.removeClass("form-error");
            } else {
                pYField.addClass("form-error");
            }
        });
    }
});

function validate(expression) {
    let node;
    try {
        node = math.parse(expression);
    } catch (err) {
        return false;
    }
    return node.compile()
}

function apply_func(expr, scope) {
    return expr.eval(scope);
}
let step_names = {1: "Load Distribution", 2: "Load Plan", 3: "Choose function",
                      4: "Load traffic", 5: "Results"};
let func_names = {1: 'ρ(w)', 2: 'S(t)', 4: "z(t)"};
let funcs = {1: '6w * (1 - w)', 2: '3t + sin(t)', 4: '4t + cos(t)'};

function generate_name(step) {
    return "Step " + step + ". " + step_names[step] + ".";
}

function get_func_name(step) {
    return "Function " + func_names[step] + ":";
}

function get_scope(step, value) {
    let scope;
    switch (step) {
        case 1:
            scope = {w: value / 100};
            break;
        case 2:
            scope = {t: value};
            break;
        case 4:
            scope = {t: value};
            break;
    }
    return scope;
}

function get_func(step) {
    return funcs[step];
}

function update_func(step, func) {
    $.post('/', {'action': "update_function", 'func_name': func_names[step], 'func': func});
    funcs[step] = func;
}
