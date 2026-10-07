// Data loader: hands the page the committed summary file. Pages never read raw trips.
import {summary} from "../../loaders/summary.js";

summary("daily.csv");
