/*
 * Copyright (C) 2011 Brockmann Consult GmbH (info@brockmann-consult.de)
 * 
 * This program is free software; you can redistribute it and/or modify it
 * under the terms of the GNU General Public License as published by the Free
 * Software Foundation; either version 3 of the License, or (at your option)
 * any later version.
 * This program is distributed in the hope that it will be useful, but WITHOUT
 * ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or
 * FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for
 * more details.
 * 
 * You should have received a copy of the GNU General Public License along
 * with this program; if not, see http://www.gnu.org/licenses/
 */


package org.esa.beam.gpf.devtools.graphgen;

import org.esa.beam.framework.dataio.ProductIO;
import org.esa.beam.framework.datamodel.Product;
import org.esa.beam.framework.gpf.GPF;
import org.esa.beam.framework.gpf.Operator;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileWriter;
import java.io.IOException;

/**
 * Test tool for the {@link GraphGen} class.
 * <pre>
 *     Usage: GraphGenMain <productPath> <graphmlPath> <operatorClass> [[<hideBands>] <hideProducts>]
 * </pre>
 *
 * @author Thomas Storm
 * @author Norman Fomferra
 */
public class GraphGenTool {

    static {
        GPF.getDefaultInstance().getOperatorSpiRegistry().loadOperatorSpis();
    }

    public static void main(String[] args) throws IOException {
        if (args.length < 3) {
            System.out.println("Usage: GraphGenMain <productPath> <graphmlPath> <operatorClass> [[<hideBands>] <hideProducts>]");
            System.exit(1);
        }
        String productPath = args[0];
        String graphmlPath = args[1];
        String opClassName = args[2];
        String hideBandsArg = args.length > 3 ? args[3] : null;
        String hideProductsArg = args.length > 4 ? args[4] : null;

        Operator operator;
        try {
            operator = (Operator) Class.forName(opClassName).newInstance();
        } catch (Exception e) {
            System.err.println("Error: Failed to create instance of " + opClassName);
            e.printStackTrace(System.err);
            System.exit(2);
            return;
        }

        Product sourceProduct = ProductIO.readProduct(new File(productPath));
        operator.setSourceProduct(sourceProduct);
        Product targetProduct = operator.getTargetProduct();

        FileWriter fileWriter = new FileWriter(new File(graphmlPath));
        BufferedWriter writer = new BufferedWriter(fileWriter);

        GraphGen graphGen = new GraphGen();
        boolean hideBands = hideBandsArg != null && Boolean.parseBoolean(hideBandsArg);
        boolean hideProducts = hideProductsArg != null && Boolean.parseBoolean(hideProductsArg);
        if (hideProducts) {
            hideBands = true;
        }
        GraphMLHandler handler = new GraphMLHandler(writer, hideBands, hideProducts);
        graphGen.generateGraph(targetProduct, handler);
        writer.close();
    }
}
